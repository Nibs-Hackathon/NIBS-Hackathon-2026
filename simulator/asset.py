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