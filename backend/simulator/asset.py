import random

from models.asset import Asset
from models.sensor import Sensor, SensorType


class SimulatedAsset:
    def __init__(self, asset: Asset):
        self.asset = asset

        # Stable baseline values used outside injected incident windows.
        self.sensors = {
            SensorType.PRESSURE: 105.0 + random.uniform(-5, 5),
            SensorType.TEMPERATURE: 72.0 + random.uniform(-3, 3),
            SensorType.FLOW: 55.0 + random.uniform(-5, 5),
            SensorType.VIBRATION: 3.0 + random.uniform(-0.5, 0.5),
            SensorType.GAS: 2.0 + random.uniform(-0.3, 0.3),
        }

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
        self._fault_target_value = None
        self._trend_counter = 0

    def tick(self, fault=None):
        """Generate one telemetry reading per sensor for this tick."""
        telemetry = []

        if fault and not self._fault_active:
            self._fault_active = True
            self._fault_sensor = fault["sensor"]
            self._fault_original_value = self.sensors.get(fault["sensor"], 100)
            self._fault_target_value = float(fault["value"])
            self._fault_ticks = 0

        for sensor_type, base_value in self.sensors.items():
            value = base_value

            if self._fault_active and sensor_type == self._fault_sensor:
                self._fault_ticks += 1

                # Begin at the injected emergency reading and recover smoothly
                # to the pre-fault baseline. The previous implementation ignored
                # fault["value"], making event severity and health contradict.
                decay_factor = max(0.0, 1.0 - ((self._fault_ticks - 1) / 8.0))
                original_value = float(self._fault_original_value)
                target_value = float(self._fault_target_value)
                value = original_value + ((target_value - original_value) * decay_factor)

                if self._fault_ticks > 8:
                    value = original_value
                    self._fault_active = False
                    self._fault_sensor = None
                    self._fault_original_value = None
                    self._fault_target_value = None
            else:
                self._trend_counter += 1
                if self._trend_counter > random.randint(10, 30):
                    self.trends[sensor_type] = random.choice([-1, 0, 1])
                    self._trend_counter = 0

                value += self.trends[sensor_type] * random.uniform(0.02, 0.08)
                value += random.gauss(0, 0.2)

                ranges = {
                    SensorType.PRESSURE: (90, 150),
                    SensorType.TEMPERATURE: (60, 90),
                    SensorType.FLOW: (30, 80),
                    SensorType.VIBRATION: (1, 8),
                    SensorType.GAS: (1, 5),
                }
                min_val, max_val = ranges.get(sensor_type, (0, 100))
                value = max(min_val, min(max_val, value))

            self.sensors[sensor_type] = value
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
