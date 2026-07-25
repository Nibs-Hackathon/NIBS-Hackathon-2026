"""Simulator with proper incident cooldown and rate limiting."""

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
            from services.notification_service import NotificationService, Notification, NotificationType, NotificationSeverity
            self._Notification = Notification
            self._NotificationType = NotificationType
            self._NotificationSeverity = NotificationSeverity
            self.notification_service = NotificationService()
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
            self._get_persistence().record_telemetry(telemetry)
        except Exception as e:
            # Log but don't crash the simulation
            print(f"⚠️ Telemetry save failed: {e}")
        
        # Update asset health
        for asset in self.facility.assets:
            history = self.state.get_history(asset.asset.id)
            if history:
                metrics = self.computation_engine.compute_asset(asset.asset, history)
                self.kernel.asset_service.update_health(asset.asset.id, metrics["health"])
                self.kernel.asset_service.update_status(asset.asset.id, metrics["status"])
        
        # ... rest of code

        # Update asset health
        for asset in self.facility.assets:
            history = self.state.get_history(asset.asset.id)
            if history:
                metrics = self.computation_engine.compute_asset(asset.asset, history)
                self.kernel.asset_service.update_health(asset.asset.id, metrics["health"])
                self.kernel.asset_service.update_status(asset.asset.id, metrics["status"])

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
        self.active_incidents[asset_id] = {
            "event": event,
            "start_time": datetime.now(),
            "tick": tick_number,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "resolved": False,
        }
        
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
        
        # ✅ Incident detected
        notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.INCIDENT_DETECTED,
                severity=NotificationSeverity.CRITICAL,
                title=f"🚨 {event.name}",
                message=f"{asset_name}",
                asset_id=asset_id,
                asset_name=asset_name,
                incident_type=event.name,
            )
        )
        
        # ✅ Revenue impact
        impact = revenue_service.calculate_incident_impact(event.name, asset_type, duration_hours=2)
        notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.REVENUE_IMPACT,
                severity=NotificationSeverity.WARNING if impact['revenue_loss'] > 1000 else NotificationSeverity.INFO,
                title="💰 Revenue Impact",
                message=f"${impact['revenue_loss']:,.0f}",
                asset_id=asset_id,
                asset_name=asset_name,
                revenue_impact=impact['revenue_loss'],
            )
        )

    def _resolve_incident(self, asset_id, tick_number, asset_name):
        """Resolve an active incident."""
        if asset_id in self.active_incidents:
            active_incident = self.active_incidents[asset_id]
            self.incident_resolution_count += 1
            
            notification_service = self._get_notification_service()
            Notification = self._Notification
            NotificationType = self._NotificationType
            NotificationSeverity = self._NotificationSeverity
            
            # ✅ Send resolution notification
            notification_service.add_notification(
                Notification(
                    id=str(uuid4()),
                    type=NotificationType.INCIDENT_RESOLVED,
                    severity=NotificationSeverity.SUCCESS,
                    title="✅ Resolved",
                    message=asset_name,
                    asset_id=asset_id,
                    asset_name=asset_name,
                )
            )

            # Persist the actual field-condition resolution.  This deliberately
            # happens here—not when the AI report completes—so audit history
            # can accurately show open incidents and resolution time.
            try:
                asset = self.kernel.asset_service.get(asset_id)
                self._get_persistence().resolve_incident(
                    getattr(active_incident.get("event"), "id", None),
                    getattr(asset, "health", None),
                )
            except Exception as error:
                print(f"Incident resolution persistence failed: {error}")
            
            # ✅ Remove from active incidents
            del self.active_incidents[asset_id]
            
            print(f"✅ Resolved: {asset_name}")

    def _check_values_normalized(self, asset_id):
        """Check if telemetry values have returned to normal range."""
        history = self.state.get_history(asset_id)
        if not history:
            return True
        
        recent = history[-5:]
        violations = 0
        
        for reading in recent:
            asset = self.kernel.asset_service.get(asset_id)
            asset_type = asset.asset_type.value if asset and hasattr(asset.asset_type, 'value') else "Pump"
            thresholds = self.config.get_thresholds(asset_type)
            
            sensor_type = reading.sensor_type.value if hasattr(reading.sensor_type, 'value') else str(reading.sensor_type)
            
            if sensor_type == "Pressure":
                if reading.value > thresholds.get("pressure_max", 150) * 0.85:
                    violations += 1
            elif sensor_type == "Temperature":
                if reading.value > thresholds.get("temperature_max", 85) * 0.85:
                    violations += 1
            elif sensor_type == "Vibration":
                if reading.value > thresholds.get("vibration_max", 8) * 0.85:
                    violations += 1
            elif sensor_type == "Gas":
                if reading.value > thresholds.get("gas_max", 40) * 0.85:
                    violations += 1
            elif sensor_type == "Flow":
                if reading.value < thresholds.get("flow_min", 25) * 1.15:
                    violations += 1
        
        return violations < 2
