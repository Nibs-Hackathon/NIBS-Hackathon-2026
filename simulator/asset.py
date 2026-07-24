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