"""Optimized event generator - ONLY generates events from injected faults."""

from mao.events.event import Event


class EventGenerator:
    
    def __init__(self):
        self._faults = []  # Store injected faults

    def add_fault(self, fault, asset_id, asset_type, health_before=None):
        """Add a fault that will generate an event."""
        self._faults.append({
            "fault": fault,
            "asset_id": asset_id,
            "asset_type": asset_type,
            "health_before": health_before,
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
            
            raw_sensor = fault.get("sensor", "")
            sensor = getattr(raw_sensor, "value", raw_sensor)
            sensor = str(sensor).strip().lower()
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
                payload={sensor: value, "asset_type": asset_type, "health_before": fault_data.get("health_before")}
            )
            events.append(event)
        
        # Clear faults after generating
        self._faults = []
        
        return events
    
    def clear_cache(self):
        """Clear all stored faults."""
        self._faults = []
