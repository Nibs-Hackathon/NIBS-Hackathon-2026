import random

from models.asset import Asset
from models.sensor import Sensor, SensorType


class SimulatedAsset:
    def __init__(self, asset: Asset, operating_thresholds=None):
        self.asset = asset
        thresholds = operating_thresholds or {}
        rng = random.Random(asset.id)

        pressure_max = float(thresholds.get("pressure_max", 150))
        temperature_max = float(thresholds.get("temperature_max", 90))
        flow_min = float(thresholds.get("flow_min", 25))
        vibration_max = float(thresholds.get("vibration_max", 8))
        gas_max = float(thresholds.get("gas_max", 40))

        # Stable, asset-specific baselines derived from the cached Gemini
        # operating envelope. No network call occurs inside tick().
        self.sensors = {
            SensorType.PRESSURE: pressure_max * rng.uniform(0.62, 0.74),
            SensorType.TEMPERATURE: temperature_max * rng.uniform(0.70, 0.82),
            SensorType.FLOW: flow_min * rng.uniform(1.8, 2.35),
            SensorType.VIBRATION: vibration_max * rng.uniform(0.28, 0.46),
            SensorType.GAS: max(1.0, gas_max * rng.uniform(0.045, 0.09)),
        }
        self.ranges = {
            SensorType.PRESSURE: (pressure_max * 0.55, pressure_max * 0.96),
            SensorType.TEMPERATURE: (temperature_max * 0.62, temperature_max * 0.96),
            SensorType.FLOW: (flow_min, flow_min * 3.0),
            SensorType.VIBRATION: (max(0.2, vibration_max * 0.12), vibration_max * 0.92),
            SensorType.GAS: (max(0.1, gas_max * 0.02), gas_max * 0.35),
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
            raw_sensor = fault["sensor"]
            fault_sensor = (
                raw_sensor
                if isinstance(raw_sensor, SensorType)
                else SensorType(str(raw_sensor).strip().capitalize())
            )
            self._fault_active = True
            self._fault_sensor = fault_sensor
            self._fault_original_value = self.sensors.get(fault_sensor, 100)
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

                min_val, max_val = self.ranges.get(sensor_type, (0, 100))
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

    def clear_fault(self):
        """Clear an injected fault so shutoff can hold the asset quiet."""
        self._fault_active = False
        self._fault_sensor = None
        self._fault_original_value = None
        self._fault_target_value = None
        self._fault_ticks = 0

    def _get_unit(self, sensor_type):
        units = {
            SensorType.PRESSURE: "PSI",
            SensorType.TEMPERATURE: "°C",
            SensorType.FLOW: "L/min",
            SensorType.VIBRATION: "mm/s",
            SensorType.GAS: "ppm",
        }
        return units.get(sensor_type, "")
