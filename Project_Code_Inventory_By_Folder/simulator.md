# Folder: simulator Code Inventory

Generated: 2026-07-24 12:23:53 UTC

Contains 6 project files.

## simulator/asset.py

**File path:** `simulator/asset.py`

```python
import random

from models.asset import Asset
from models.sensor import Sensor, SensorType


class SimulatedAsset:

    def __init__(self, asset: Asset):

        self.asset = asset

        self.sensors = {
            SensorType.PRESSURE: 110,
            SensorType.TEMPERATURE: 70,
            SensorType.FLOW: 60,
            SensorType.VIBRATION: 15,
            SensorType.GAS: 5,
        }


    def tick(self, fault=None):

        telemetry = []

        for sensor, value in self.sensors.items():

            if (
                fault is not None
                and fault["sensor"] == sensor
            ):

                value = fault["value"]

            else:

                value += random.uniform(-2, 2)


            self.sensors[sensor] = value


            telemetry.append(
                Sensor(
                    id=f"{self.asset.id}_{sensor.value}",
                    asset_id=self.asset.id,
                    sensor_type=sensor,
                    value=round(value, 2),
                    unit="",
                )
            )


        return telemetry
```

## simulator/event_generator.py

**File path:** `simulator/event_generator.py`

```python
"""Optimized event generator with precomputed thresholds - NO circular imports."""

from mao.events.event import Event
from models.sensor import SensorType
from services.config_services import ConfigService
from functools import lru_cache


class EventGenerator:
    
    def __init__(self):
        self.config = ConfigService()
        self._kernel = None  # Lazy load
        self._threshold_cache = {}

    @property
    def kernel(self):
        """Lazy load kernel to avoid circular import."""
        if self._kernel is None:
            from services.runtime import get_kernel
            self._kernel = get_kernel()
        return self._kernel

    @lru_cache(maxsize=500)
    def _get_asset_type(self, asset_id: str) -> str:
        """Cache asset type lookups."""
        asset = self.kernel.asset_service.get(asset_id)
        if not asset:
            return "Pump"
        return asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type)

    def generate(self, telemetry):
        """Fast event generation with cached thresholds."""
        events = []
        
        if not telemetry:
            return events
        
        # Group readings by asset_id for batch processing
        readings_by_asset = {}
        for reading in telemetry:
            asset_id = reading.asset_id
            if asset_id not in readings_by_asset:
                readings_by_asset[asset_id] = []
            readings_by_asset[asset_id].append(reading)
        
        # Process each asset's readings
        for asset_id, readings in readings_by_asset.items():
            # Get asset type once per asset
            asset_type = self._get_asset_type(asset_id)
            
            # Get thresholds once per asset type
            cache_key = f"thresholds_{asset_type}"
            if cache_key not in self._threshold_cache:
                self._threshold_cache[cache_key] = self.config.get_thresholds(asset_type)
            thresholds = self._threshold_cache[cache_key]
            
            # Check all readings for this asset
            for reading in readings:
                event = self._check_threshold(reading, thresholds, asset_type)
                if event:
                    events.append(event)
        
        return events

    def _check_threshold(self, reading, thresholds, asset_type):
        """Single check with precomputed thresholds."""
        sensor_type = reading.sensor_type
        
        if sensor_type == SensorType.PRESSURE:
            if reading.value > thresholds.get("pressure_max", 150):
                return Event(
                    name="PressureSpike",
                    source=reading.asset_id,
                    payload={"pressure": reading.value, "asset_type": asset_type}
                )
        
        elif sensor_type == SensorType.TEMPERATURE:
            if reading.value > thresholds.get("temperature_max", 85):
                return Event(
                    name="HighTemperature",
                    source=reading.asset_id,
                    payload={"temperature": reading.value, "asset_type": asset_type}
                )
        
        elif sensor_type == SensorType.GAS:
            if reading.value > thresholds.get("gas_max", 40):
                return Event(
                    name="GasLeak",
                    source=reading.asset_id,
                    payload={"gas": reading.value, "asset_type": asset_type}
                )
        
        elif sensor_type == SensorType.VIBRATION:
            if reading.value > thresholds.get("vibration_max", 8):
                return Event(
                    name="HighVibration",
                    source=reading.asset_id,
                    payload={"vibration": reading.value, "asset_type": asset_type}
                )
        
        elif sensor_type == SensorType.FLOW:
            if reading.value < thresholds.get("flow_min", 25):
                return Event(
                    name="FlowRestriction",
                    source=reading.asset_id,
                    payload={"flow": reading.value, "asset_type": asset_type}
                )
        
        return None
    
    def clear_cache(self):
        """Clear all caches."""
        self._threshold_cache.clear()
        self._get_asset_type.cache_clear()
```

## simulator/facility.py

**File path:** `simulator/facility.py`

```python
from models.facility import Facility
from simulator.asset import SimulatedAsset
from models.sensor import SensorType


class SimulatedFacility:
    def __init__(self, facility: Facility):
        self.assets = [
            SimulatedAsset(asset)
            for asset in facility.assets
        ]
        # ✅ Track active faults per asset
        self.active_faults = {}  # asset_id -> {"sensor": sensor, "value": value, "tick": tick}

    def tick(self, tick_number, fault=None, target_asset_id=None):
        """Generate telemetry with optional targeted fault."""
        telemetry = []
        
        for asset in self.assets:
            # ✅ Check if this asset has an active fault
            current_fault = None
            
            if target_asset_id and asset.asset.id == target_asset_id:
                # ✅ New fault for this asset
                current_fault = fault
                if fault:
                    self.active_faults[asset.asset.id] = {
                        "sensor": fault.get("sensor"),
                        "value": fault.get("value"),
                        "tick": tick_number,
                        "active": True
                    }
            elif asset.asset.id in self.active_faults:
                # ✅ Check if fault should still be active (for 2-3 ticks only)
                fault_data = self.active_faults[asset.asset.id]
                if fault_data.get("active", False):
                    # ✅ Fault lasts only 2-3 ticks, then it's "fixed" by agents
                    ticks_active = tick_number - fault_data.get("tick", tick_number)
                    if ticks_active > 3:  # ✅ Agents "fixed" it after 3 ticks
                        fault_data["active"] = False
                        print(f"✅ Fault resolved for {asset.asset.name} after {ticks_active} ticks")
                    else:
                        # ✅ Still active - reapply the fault
                        current_fault = {
                            "sensor": fault_data.get("sensor"),
                            "value": fault_data.get("value")
                        }
            
            telemetry.extend(asset.tick(fault=current_fault))
        
        return telemetry
```

## simulator/fault_injector.py

**File path:** `simulator/fault_injector.py`

```python
class FaultInjector:

    def __init__(self):

        self.schedule_map = {}

    def schedule(self, tick, asset_index, sensor, value):

        self.schedule_map[(tick, asset_index)] = {
            "sensor": sensor,
            "value": value,
        }

    def get_fault(self, tick, asset_index):

        return self.schedule_map.get((tick, asset_index))
```

## simulator/sensor.py

**File path:** `simulator/sensor.py`

```python

```

## simulator/simulator.py

**File path:** `simulator/simulator.py`

```python
"""Simulator with automated incident detection and cooldown."""

import random
from datetime import datetime
from uuid import uuid4

from simulator.event_generator import EventGenerator
from services.persistence import PersistenceService
from services.computation_engine import ComputationEngine
from services.notification_service import NotificationService, Notification, NotificationType, NotificationSeverity
from services.revenue_impact_calculator import revenue_service
from services.maintenance_scheduler import maintenance_scheduler
from services.ai_config import AIConfigGenerator


class Simulator:
    def __init__(self, facility, kernel):
        self.facility = facility
        self.kernel = kernel
        self.state = kernel.state
        self.generator = EventGenerator()
        self.persistence = PersistenceService()
        self.computation_engine = ComputationEngine()
        self.notification_service = NotificationService()
        self.config = AIConfigGenerator()
        
        # ✅ Track active incidents with cooldown
        self.active_incidents = {}  # asset_id -> {"event": event, "start_time": time, "cooldown_until": tick}
        self.incident_resolution_count = 0
        self._last_incident_time = 0
        self._incident_cooldown_ticks = 10  # ✅ No new incidents for 10 ticks after resolution

    def tick(self, tick_number, fault=None, target_asset_id=None):
        """Run one simulation tick with optional targeted fault."""
        
        # ✅ Generate telemetry with fault
        telemetry = self.facility.tick(tick_number, fault, target_asset_id)
        self.state.add_telemetry(telemetry)
        self.persistence.record_telemetry(telemetry)

        # ✅ Update asset health
        for asset in self.facility.assets:
            history = self.state.get_history(asset.asset.id)
            metrics = self.computation_engine.compute_asset(asset.asset, history)
            
            self.kernel.asset_service.update_health(
                asset.asset.id,
                metrics["health"],
            )
            self.kernel.asset_service.update_status(
                asset.asset.id,
                metrics["status"],
            )

        # ✅ AUTO-INCIDENT DETECTION - WITH COOLDOWN
        reports = []
        events = self.generator.generate(telemetry)

        for event in events:
            asset_id = event.source
            asset = self.kernel.asset_service.get(asset_id)
            asset_name = asset.name if asset else asset_id
            
            # ✅ Check if asset has an active incident or is in cooldown
            if asset_id in self.active_incidents:
                incident_data = self.active_incidents[asset_id]
                # ✅ Check if incident is resolved (values normalized)
                if self._check_values_normalized(asset_id):
                    self._resolve_incident(asset_id, asset_name, event)
                    # ✅ Add cooldown after resolution
                    self.active_incidents[asset_id]["resolved_at"] = tick_number
                continue  # Skip new incident
            
            # ✅ Check cooldown for recently resolved incidents
            if asset_id in self._get_recently_resolved():
                continue  # Skip during cooldown
            
            # ✅ NEW INCIDENT DETECTED
            self._trigger_incident(event, asset, asset_name, tick_number)

        return telemetry, reports

    def _get_recently_resolved(self):
        """Get assets in cooldown period."""
        resolved_assets = []
        for asset_id, data in self.active_incidents.items():
            if data.get("resolved_at"):
                cooldown_ticks = data.get("cooldown_until", 0)
                if cooldown_ticks > 0:
                    resolved_assets.append(asset_id)
        return resolved_assets

    def _trigger_incident(self, event, asset, asset_name, tick_number):
        """Trigger a new incident with full notification flow."""
        
        asset_id = event.source
        asset_type = asset.asset_type.value if asset and hasattr(asset.asset_type, 'value') else "Pump"
        
        # ✅ Store active incident
        self.active_incidents[asset_id] = {
            "event": event,
            "start_time": datetime.now(),
            "tick": tick_number,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "resolved_at": None,
            "cooldown_until": tick_number + 10,  # ✅ 10 tick cooldown
        }
        
        # ✅ Run MAO agents
        report = self.kernel.handle_event(event)
        
        # ✅ Send notifications
        self._send_notifications(event, asset_name, asset_id, asset_type)
        
        return report

    def _send_notifications(self, event, asset_name, asset_id, asset_type):
        """Send notifications for an incident."""
        
        # ✅ Only send if not already sent (avoid duplicates)
        if self.active_incidents.get(asset_id, {}).get("notifications_sent", False):
            return
        
        # ✅ Mark notifications as sent
        self.active_incidents[asset_id]["notifications_sent"] = True
        
        # ✅ 1. Incident Detected
        self.notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.INCIDENT_DETECTED,
                severity=NotificationSeverity.CRITICAL,
                title=f"🚨 {event.name} DETECTED",
                message=f"Automated detection on {asset_name}",
                asset_id=asset_id,
                asset_name=asset_name,
                incident_type=event.name,
            )
        )
        
        # ✅ 2. Agents Working
        self.notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.AGENTS_WORKING,
                severity=NotificationSeverity.WARNING,
                title="⚡ AGENTS WORKING",
                message=f"AI agents analyzing {event.name} on {asset_name}",
                asset_id=asset_id,
                asset_name=asset_name,
                incident_type=event.name,
            )
        )
        
        # ✅ 3. Revenue Impact
        impact = revenue_service.calculate_incident_impact(
            event.name, 
            asset_type,
            duration_hours=2
        )
        self.notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.REVENUE_IMPACT,
                severity=NotificationSeverity.WARNING if impact['revenue_loss'] > 1000 else NotificationSeverity.INFO,
                title="💰 REVENUE IMPACT",
                message=f"Estimated loss: ${impact['revenue_loss']:,.2f}",
                asset_id=asset_id,
                asset_name=asset_name,
                incident_type=event.name,
                revenue_impact=impact['revenue_loss'],
            )
        )

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
                if reading.value > thresholds.get("pressure_max", 150):
                    violations += 1
            elif sensor_type == "Temperature":
                if reading.value > thresholds.get("temperature_max", 85):
                    violations += 1
            elif sensor_type == "Vibration":
                if reading.value > thresholds.get("vibration_max", 8):
                    violations += 1
            elif sensor_type == "Gas":
                if reading.value > thresholds.get("gas_max", 40):
                    violations += 1
            elif sensor_type == "Flow":
                if reading.value < thresholds.get("flow_min", 25):
                    violations += 1
        
        return violations < 2

    def _resolve_incident(self, asset_id, asset_name, event):
        """Resolve an active incident."""
        if asset_id in self.active_incidents:
            self.active_incidents[asset_id]["resolved_at"] = datetime.now()
            self.incident_resolution_count += 1
            
            # ✅ Send resolution notification
            self.notification_service.add_notification(
                Notification(
                    id=str(uuid4()),
                    type=NotificationType.INCIDENT_RESOLVED,
                    severity=NotificationSeverity.SUCCESS,
                    title="✅ INCIDENT RESOLVED",
                    message=f"{event.name} on {asset_name} has been resolved",
                    asset_id=asset_id,
                    asset_name=asset_name,
                    incident_type=event.name,
                )
            )
            
            # ✅ Schedule maintenance if health is still low
            asset = self.kernel.asset_service.get(asset_id)
            history = self.state.get_history(asset_id)
            metrics = self.computation_engine.compute_asset(asset, history)
            
            if metrics.get("health", 100) < 80:
                task = maintenance_scheduler.schedule_maintenance(
                    {"id": asset_id, "name": asset_name, "type": asset.asset_type.value if asset else "Pump"},
                    metrics
                )
                if task:
                    self.notification_service.add_notification(
                        Notification(
                            id=str(uuid4()),
                            type=NotificationType.MAINTENANCE_SCHEDULED,
                            severity=NotificationSeverity.INFO,
                            title="🔧 MAINTENANCE SCHEDULED",
                            message=f"Maintenance for {asset_name} on {task.scheduled_date.strftime('%b %d, %H:%M')}",
                            asset_id=asset_id,
                            asset_name=asset_name,
                            maintenance_scheduled=task.scheduled_date.strftime("%Y-%m-%d %H:%M"),
                        )
                    )
```
