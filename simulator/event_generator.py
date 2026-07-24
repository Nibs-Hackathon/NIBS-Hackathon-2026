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