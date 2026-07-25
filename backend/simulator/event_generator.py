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