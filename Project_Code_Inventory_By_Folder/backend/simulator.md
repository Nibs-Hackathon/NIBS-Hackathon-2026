# Folder: backend/simulator Code Inventory

Generated: 2026-07-25T06:14:25 UTC

Contains 6 project files.

## backend/simulator/asset.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/asset.py`

```python
import random
import math
from models.asset import Asset
from models.sensor import Sensor, SensorType


class SimulatedAsset:
    def __init__(self, asset: Asset):
        self.asset = asset
        
        # ✅ Base values with realistic ranges - STABLE by default
        self.sensors = {
            SensorType.PRESSURE: 105.0 + random.uniform(-5, 5),   # Stable around 100-110
            SensorType.TEMPERATURE: 72.0 + random.uniform(-3, 3), # Stable around 69-75
            SensorType.FLOW: 55.0 + random.uniform(-5, 5),        # Stable around 50-60
            SensorType.VIBRATION: 3.0 + random.uniform(-0.5, 0.5),# Stable around 2.5-3.5
            SensorType.GAS: 2.0 + random.uniform(-0.3, 0.3),      # Stable around 1.7-2.3
        }
        
        # ✅ Very slow trend changes
        self.trends = {
            SensorType.PRESSURE: 0,
            SensorType.TEMPERATURE: 0,
            SensorType.FLOW: 0,
            SensorType.VIBRATION: 0,
            SensorType.GAS: 0,
        }
        
        self.degradation = 0.0
        self._fault_active = False
        self._fault_sensor = None
        self._fault_ticks = 0
        self._fault_original_value = None
        self._trend_counter = 0  # ✅ Track how long since last trend change

    def tick(self, fault=None):
        """Generate telemetry for one tick."""
        telemetry = []
        
        # ✅ Handle fault
        if fault and not self._fault_active:
            self._fault_active = True
            self._fault_sensor = fault["sensor"]
            self._fault_original_value = self.sensors.get(fault["sensor"], 100)
            self._fault_ticks = 0
        
        for sensor_type, base_value in self.sensors.items():
            value = base_value
            
            # ✅ Apply active fault
            if self._fault_active and sensor_type == self._fault_sensor:
                self._fault_ticks += 1
                
                # ✅ Fault decays back to normal over 5-8 ticks
                decay_factor = max(0, 1 - (self._fault_ticks / 8))
                if self._fault_original_value:
                    target_value = self._fault_original_value * (1 + random.uniform(-0.03, 0.03))
                    value = target_value + (self._fault_original_value * 0.3 * decay_factor)
                    
                    # ✅ Clamp to realistic range
                    if sensor_type == SensorType.PRESSURE:
                        value = min(160, max(90, value))
                    elif sensor_type == SensorType.TEMPERATURE:
                        value = min(95, max(60, value))
                    elif sensor_type == SensorType.VIBRATION:
                        value = min(12, max(2, value))
                    
                    # ✅ If decayed enough, deactivate fault
                    if self._fault_ticks > 8 or abs(value - self._fault_original_value) < 2:
                        self._fault_active = False
                        self._fault_sensor = None
                        self._fault_original_value = None
                        value = self._fault_original_value if self._fault_original_value else base_value
                else:
                    value = base_value
                    self._fault_active = False
            
            else:
                # ✅ Normal variation - VERY STABLE
                # Change trend direction only occasionally
                self._trend_counter += 1
                if self._trend_counter > random.randint(10, 30):  # Change every 10-30 ticks
                    self.trends[sensor_type] = random.choice([-1, 0, 1])
                    self._trend_counter = 0
                
                # ✅ Apply trend very slowly
                value += self.trends[sensor_type] * random.uniform(0.02, 0.08)  # Very slow change
                
                # ✅ Add tiny natural noise
                value += random.gauss(0, 0.2)  # Very small noise
                
                # ✅ Keep within realistic ranges
                ranges = {
                    SensorType.PRESSURE: (90, 150),
                    SensorType.TEMPERATURE: (60, 90),
                    SensorType.FLOW: (30, 80),
                    SensorType.VIBRATION: (1, 8),
                    SensorType.GAS: (1, 5),
                }
                min_val, max_val = ranges.get(sensor_type, (0, 100))
                value = max(min_val, min(max_val, value))
            
            # ✅ Store updated value
            self.sensors[sensor_type] = value
            
            # ✅ Create telemetry reading
            telemetry.append(
                Sensor(
                    id=f"{self.asset.id}_{sensor_type.value}",
                    asset_id=self.asset.id,
                    sensor_type=sensor_type,
                    value=round(value, 2),
                    unit=self._get_unit(sensor_type),
                )
            )
        
        return telemetry

    def _get_unit(self, sensor_type):
        units = {
            SensorType.PRESSURE: "PSI",
            SensorType.TEMPERATURE: "°C",
            SensorType.FLOW: "L/min",
            SensorType.VIBRATION: "mm/s",
            SensorType.GAS: "ppm",
        }
        return units.get(sensor_type, "")
```

## backend/simulator/event_generator.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/event_generator.py`

```python
"""Optimized event generator - ONLY generates events from injected faults."""

from mao.events.event import Event


class EventGenerator:
    
    def __init__(self):
        self._faults = []  # Store injected faults

    def add_fault(self, fault, asset_id, asset_type):
        """Add a fault that will generate an event."""
        self._faults.append({
            "fault": fault,
            "asset_id": asset_id,
            "asset_type": asset_type
        })

    def generate(self, telemetry):
        """
        ✅ ONLY generate events from injected faults.
        No auto-detection from telemetry.
        """
        events = []
        
        if not self._faults:
            return events
        
        # Process each fault
        for fault_data in self._faults:
            fault = fault_data["fault"]
            asset_id = fault_data["asset_id"]
            asset_type = fault_data["asset_type"]
            
            sensor = fault.get("sensor", "")
            value = fault.get("value", 0)
            
            # Map sensor to event name
            event_map = {
                "pressure": "PressureSpike",
                "temperature": "HighTemperature",
                "vibration": "HighVibration",
                "gas": "GasLeak",
                "flow": "FlowRestriction",
            }
            
            event_name = event_map.get(sensor, "Unknown")
            
            event = Event(
                name=event_name,
                source=asset_id,
                payload={sensor: value, "asset_type": asset_type}
            )
            events.append(event)
        
        # Clear faults after generating
        self._faults = []
        
        return events
    
    def clear_cache(self):
        """Clear all stored faults."""
        self._faults = []
```

## backend/simulator/facility.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/facility.py`

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
        self.active_faults = {}

    def tick(self, tick_number, fault=None, target_asset_id=None):
        """Generate telemetry with optional targeted fault."""
        telemetry = []
        
        for asset in self.assets:
            current_fault = None
            
            # ✅ Check if this asset has an active fault
            if target_asset_id and asset.asset.id == target_asset_id:
                if fault:
                    current_fault = fault
                    self.active_faults[asset.asset.id] = {
                        "sensor": fault.get("sensor"),
                        "value": fault.get("value"),
                        "tick": tick_number,
                        "active": True
                    }
            elif asset.asset.id in self.active_faults:
                fault_data = self.active_faults[asset.asset.id]
                if fault_data.get("active", False):
                    ticks_active = tick_number - fault_data.get("tick", tick_number)
                    # ✅ Fault lasts 5 ticks then auto-resolves
                    if ticks_active > 5:
                        fault_data["active"] = False
                        print(f"✅ Fault resolved for {asset.asset.name} after {ticks_active} ticks")
                    else:
                        current_fault = {
                            "sensor": fault_data.get("sensor"),
                            "value": fault_data.get("value")
                        }
            
            telemetry.extend(asset.tick(fault=current_fault))
        
        return telemetry
```

## backend/simulator/fault_injector.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/fault_injector.py`

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

## backend/simulator/sensor.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/sensor.py`

```python

```

## backend/simulator/simulator.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/simulator.py`

```python
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
            self._get_generator().add_fault(fault, target_asset_id, asset_type)

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
```
