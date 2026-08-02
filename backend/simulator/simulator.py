"""Simulator with proper incident cooldown and rate limiting."""

import os
import random
from datetime import datetime
from uuid import uuid4
import time

from services.computation_engine import ComputationEngine
from services.revenue_impact_calculator import revenue_service
from services.maintenance_scheduler import maintenance_scheduler
from services.ai_config import AIConfigGenerator


class Simulator:
    def __init__(self, facility, kernel):
        self.facility = facility
        self.kernel = kernel
        self.state = kernel.state
        
        # ✅ Lazy load these
        self.generator = None
        self.persistence = None
        self.computation_engine = ComputationEngine()
        self.notification_service = None
        self.config = AIConfigGenerator()
        
        # ✅ Track active incidents with proper cooldown
        self.active_incidents = {}        # asset_id -> incident_data
        self.resolved_incidents = {}      # asset_id -> resolution_tick
        self.incident_resolutions = {}    # incident_id -> auditable outcome
        self._held_offline = set()        # agent shutoff holds until field work
        self._incident_cooldown_ticks = 20  # ✅ 20 ticks cooldown
        self._last_incident_time = 0
        self.incident_resolution_count = 0
        self._notification_sent = {}
        self._incident_count = 0

    def _get_generator(self):
        if self.generator is None:
            from simulator.event_generator import EventGenerator
            self.generator = EventGenerator()
        return self.generator

    def _get_persistence(self):
        if self.persistence is None:
            from services.persistence import get_persistence
            self.persistence = get_persistence()
        return self.persistence

    def _get_notification_service(self):
        if self.notification_service is None:
            from services.notification_service import notification_service, Notification, NotificationType, NotificationSeverity
            self._Notification = Notification
            self._NotificationType = NotificationType
            self._NotificationSeverity = NotificationSeverity
            self.notification_service = notification_service
        return self.notification_service

    def tick(self, tick_number, fault=None, target_asset_id=None):
        """Run one simulation tick."""
        health_before_fault = None
        if fault and target_asset_id:
            target_asset = self.kernel.asset_service.get(target_asset_id)
            health_before_fault = getattr(target_asset, "health", None) if target_asset else None
        
        # Generate telemetry
        telemetry = self.facility.tick(tick_number, fault, target_asset_id)
        self.state.add_telemetry(telemetry)
        
        # ✅ Use the fixed persistence
        try:
            persist_every = max(1, int(os.getenv("RIGOS_TELEMETRY_PERSIST_EVERY", "5")))
            if fault or tick_number % persist_every == 0:
                self._get_persistence().record_telemetry(telemetry)
        except Exception as e:
            # Log but don't crash the simulation
            print(f"⚠️ Telemetry save failed: {e}")
        
        # Update asset health
        for asset in self.facility.assets:
            history = self.state.get_history(asset.asset.id)
            if history:
                metrics = self.computation_engine.compute_asset(asset.asset, history)
                active = self.active_incidents.get(asset.asset.id)
                health = metrics["health"]
                status = metrics["status"]
                if active:
                    health = min(health, active.get("incident_health", health))
                    status = active.get("asset_status", "Attention")
                # Agent shutoff / maintenance holds beat auto telemetry status.
                held = str(getattr(asset.asset, "status", "") or "")
                if asset.asset.id in self._held_offline or held.lower() in {"offline", "maintenance"}:
                    status = "Offline" if asset.asset.id in self._held_offline else held
                self.kernel.asset_service.update_health(asset.asset.id, health)
                self.kernel.asset_service.update_status(asset.asset.id, status)
        
        # EventGenerator emits each injected event once. Recheck every active
        # incident on every tick so the operational state closes when its
        # sensor has actually returned to a safe range.
        for asset_id, incident in list(self.active_incidents.items()):
            if self._check_values_normalized(asset_id):
                asset = self.kernel.asset_service.get(asset_id)
                asset_name = asset.name if asset else incident.get("asset_name", asset_id)
                self._resolve_incident(asset_id, tick_number, asset_name)
                self.resolved_incidents[asset_id] = tick_number

        # ✅ Add injected fault to generator if present
        if fault and target_asset_id:
            asset = self.kernel.asset_service.get(target_asset_id)
            asset_type = asset.asset_type.value if asset and hasattr(asset.asset_type, 'value') else "Pump"
            self._get_generator().add_fault(fault, target_asset_id, asset_type, health_before=health_before_fault)

        # ✅ Process events - ONLY from injected faults
        reports = []
        events = self._get_generator().generate(telemetry)
        
        for event in events:
            asset_id = event.source
            
            # ✅ Check if asset is in cooldown
            if asset_id in self.resolved_incidents:
                resolved_tick = self.resolved_incidents[asset_id]
                if tick_number - resolved_tick < self._incident_cooldown_ticks:
                    continue  # ✅ Skip during cooldown
                else:
                    del self.resolved_incidents[asset_id]
            
            # ✅ Check if incident already active
            if asset_id in self.active_incidents:
                # ✅ Check if values normalized
                if self._check_values_normalized(asset_id):
                    asset = self.kernel.asset_service.get(asset_id)
                    asset_name = asset.name if asset else asset_id
                    self._resolve_incident(asset_id, tick_number, asset_name)
                    self.resolved_incidents[asset_id] = tick_number
                continue  # ✅ Don't trigger new incident
            
            # ✅ TRIGGER NEW INCIDENT
            asset = self.kernel.asset_service.get(asset_id)
            asset_name = asset.name if asset else asset_id
            report = self._trigger_incident(event, asset, asset_name, tick_number)
            if report:
                reports.append(report)

        return telemetry, reports

    def _can_trigger_for_asset(self, asset_id, tick_number):
        """Check if an asset can have a new incident."""
        if asset_id in self.resolved_incidents:
            resolved_tick = self.resolved_incidents[asset_id]
            if tick_number - resolved_tick < self._incident_cooldown_ticks:
                return False
            else:
                del self.resolved_incidents[asset_id]
        
        if asset_id in self.active_incidents:
            return False
        
        return True

    def _trigger_incident(self, event, asset, asset_name, tick_number):
        """Trigger a new incident."""
        
        asset_id = event.source
        asset_type = asset.asset_type.value if asset and hasattr(asset.asset_type, 'value') else "Pump"
        
        # ✅ Store active incident
        severity = str(getattr(event, "severity", "") or "").lower()
        penalty = 28 if "critical" in severity else 18
        current_health = float(getattr(asset, "health", 100) or 100)
        incident_health = max(0, min(current_health, current_health - penalty))
        asset_status = "Critical" if "critical" in severity else "Attention"
        self.active_incidents[asset_id] = {
            "event": event,
            "start_time": datetime.now(),
            "tick": tick_number,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "resolved": False,
            "incident_health": incident_health,
            "asset_status": asset_status,
        }
        if asset:
            self.kernel.asset_service.update_health(asset_id, incident_health)
            self.kernel.asset_service.update_status(asset_id, asset_status)
        
        self._last_incident_time = tick_number
        self._notification_sent[asset_id] = False
        
        # ✅ Run MAO agents
        report = self.kernel.handle_event(event)
        self._incident_count += 1
        
        # ✅ Send notifications (only once)
        self._send_notifications(event, asset_name, asset_id, asset_type)
        
        print(f"🚨 Incident #{self._incident_count}: {event.name} on {asset_name}")
        
        return report

    def _send_notifications(self, event, asset_name, asset_id, asset_type):
        """Send notifications for an incident (only once)."""
        
        if self._notification_sent.get(asset_id, False):
            return
        
        self._notification_sent[asset_id] = True
        
        notification_service = self._get_notification_service()
        Notification = self._Notification
        NotificationType = self._NotificationType
        NotificationSeverity = self._NotificationSeverity
        asset = self.kernel.asset_service.get(asset_id)
        refinery_name = getattr(asset, "location", None)
        notification_title = " · ".join(
            value for value in (asset_name, refinery_name) if value
        )
        
        # ✅ Incident detected
        notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.INCIDENT_DETECTED,
                severity=NotificationSeverity.CRITICAL,
                title=notification_title,
                message=event.name,
                asset_id=asset_id,
                asset_name=asset_name,
                refinery_name=refinery_name,
                incident_type=event.name,
                metadata={"incident_id": getattr(event, "id", None)},
            )
        )
        
        # ✅ Revenue impact
        impact = revenue_service.calculate_incident_impact(event.name, asset_type, duration_hours=2)
        notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.REVENUE_IMPACT,
                severity=NotificationSeverity.WARNING if impact['revenue_loss'] > 1000 else NotificationSeverity.INFO,
                title=notification_title,
                message=f"Revenue impact: ${impact['revenue_loss']:,.0f}",
                asset_id=asset_id,
                asset_name=asset_name,
                refinery_name=refinery_name,
                incident_type=event.name,
                revenue_impact=impact['revenue_loss'],
                metadata={"incident_id": getattr(event, "id", None)},
            )
        )

    def _resolve_incident(self, asset_id, tick_number, asset_name):
        """Resolve an active incident."""
        if asset_id in self.active_incidents:
            active_incident = self.active_incidents[asset_id]
            event = active_incident.get("event")
            incident_id = getattr(event, "id", None)
            resolved_at = datetime.now()
            started_at = active_incident.get("start_time")
            self.incident_resolution_count += 1
            
            notification_service = self._get_notification_service()
            Notification = self._Notification
            NotificationType = self._NotificationType
            NotificationSeverity = self._NotificationSeverity
            asset = self.kernel.asset_service.get(asset_id)
            refinery_name = getattr(asset, "location", None)
            incident_type = getattr(event, "name", None)
            notification_title = " · ".join(
                value for value in (asset_name, refinery_name) if value
            )
            
            # ✅ Send resolution notification
            notification_service.add_notification(
                Notification(
                    id=str(uuid4()),
                    type=NotificationType.INCIDENT_RESOLVED,
                    severity=NotificationSeverity.SUCCESS,
                    title=notification_title,
                    message=f"Resolved: {incident_type or 'incident'}",
                    asset_id=asset_id,
                    asset_name=asset_name,
                    refinery_name=refinery_name,
                    incident_type=incident_type,
                    metadata={"incident_id": incident_id},
                )
            )

            # Persist the actual field-condition resolution.  This deliberately
            # happens here—not when the AI report completes—so audit history
            # can accurately show open incidents and resolution time.
            try:
                self._get_persistence().resolve_incident(
                    getattr(active_incident.get("event"), "id", None),
                    getattr(asset, "health", None),
                )
            except Exception as error:
                print(f"Incident resolution persistence failed: {error}")
            
            # ✅ Remove from active incidents
            held_offline = bool(active_incident.get("agent_shut_off"))
            del self.active_incidents[asset_id]
            asset = self.kernel.asset_service.get(asset_id)
            if asset:
                history = self.state.get_history(asset_id)
                metrics = self.computation_engine.compute_asset(asset, history) if history else None
                if held_offline:
                    # Agent isolation remains until audited field work completes.
                    self.kernel.asset_service.update_status(asset_id, "Offline")
                    if metrics:
                        self.kernel.asset_service.update_health(
                            asset_id, min(float(metrics["health"]), 35.0)
                        )
                    self._held_offline.add(asset_id)
                elif metrics:
                    self.kernel.asset_service.update_health(asset_id, metrics["health"])
                    self.kernel.asset_service.update_status(asset_id, metrics["status"])
            if incident_id:
                self.incident_resolutions[str(incident_id)] = {
                    "incident_id": incident_id,
                    "asset_id": asset_id,
                    "resolved_at": resolved_at,
                    "resolution_seconds": (
                        round(max(0.0, (resolved_at - started_at).total_seconds()), 2)
                        if started_at else None
                    ),
                    "health_after": getattr(
                        self.kernel.asset_service.get(asset_id),
                        "health",
                        None,
                    ),
                }
            
            print(f"✅ Resolved: {asset_name}")

    def complete_field_work(self, asset_id, incident_id=None):
        """Resolve the matching incident after audited simulated field work.

        This updates only RigOS simulation state and never commands physical
        industrial equipment.
        """
        active = self.active_incidents.get(asset_id)
        if active is None:
            # Restart after agent shutoff even if the spike already normalized.
            if asset_id in self._held_offline:
                self._held_offline.discard(asset_id)
                self.kernel.asset_service.update_status(asset_id, "Running")
                prior = self.incident_resolutions.get(str(incident_id)) if incident_id else None
                return {
                    "resolved": True,
                    "already_resolved": True,
                    "asset_id": asset_id,
                    "incident_id": incident_id,
                    "reason": "Agent shutoff cleared after field work",
                    **(prior or {}),
                }
            prior = self.incident_resolutions.get(str(incident_id)) if incident_id else None
            if prior:
                return {
                    "resolved": True,
                    "already_resolved": True,
                    **prior,
                    "reason": "The linked simulator incident was already resolved",
                }
            return {
                "resolved": False,
                "incident_id": incident_id,
                "reason": "No active simulator incident exists for this asset",
            }
        event = active.get("event")
        active_incident_id = getattr(event, "id", None)
        if incident_id and str(active_incident_id) != str(incident_id):
            return {
                "resolved": False,
                "incident_id": incident_id,
                "reason": "The work order is linked to a different incident",
            }
        asset = self.kernel.asset_service.get(asset_id)
        asset_name = getattr(asset, "name", active.get("asset_name", asset_id))
        # Clear agent isolation so resolve can restore modelled running status.
        active["agent_shut_off"] = False
        self._held_offline.discard(asset_id)
        resolution_tick = int(time.time())
        self._resolve_incident(asset_id, resolution_tick, asset_name)
        self.resolved_incidents[asset_id] = resolution_tick
        if asset and str(getattr(asset, "status", "")).lower() == "offline":
            self.kernel.asset_service.update_status(asset_id, "Running")
        return {
            "resolved": True,
            "incident_id": active_incident_id,
            "asset_id": asset_id,
            "reason": "Field work completed in RigOS simulation",
        }

    def _check_values_normalized(self, asset_id):
        """Check if telemetry values have returned to normal range."""
        history = self.state.get_history(asset_id)
        incident = self.active_incidents.get(asset_id)
        event = incident.get("event") if incident else None
        payload = getattr(event, "payload", {}) or {}
        sensor_name = next(
            (
                name
                for name in ("pressure", "temperature", "vibration", "gas", "flow")
                if name in payload
            ),
            None,
        )
        if not history or not sensor_name:
            return False

        relevant = [
            reading
            for reading in history
            if str(
                getattr(getattr(reading, "sensor_type", None), "value", "")
            ).lower() == sensor_name
        ][-3:]
        if len(relevant) < 3:
            return False

        asset = self.kernel.asset_service.get(asset_id)
        asset_type = (
            asset.asset_type.value
            if asset and hasattr(asset.asset_type, "value")
            else "Pump"
        )
        thresholds = self.config.get_thresholds(asset_type)
        if sensor_name == "flow":
            limit = thresholds.get("flow_min", 25)
            return all(reading.value >= limit for reading in relevant)

        limit = thresholds.get(f"{sensor_name}_max")
        return bool(limit) and all(reading.value <= limit for reading in relevant)
