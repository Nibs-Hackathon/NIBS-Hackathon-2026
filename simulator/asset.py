import random

from models.asset import Asset
from models.sensor import Sensor, SensorType

<<<<<<< HEAD
class SimulatedAsset:
    def __init__(self, asset: Asset):
=======

class SimulatedAsset:

    def __init__(self, asset: Asset):

>>>>>>> origin/dev-ashutosh-zinia
        self.asset = asset

        self.sensors = {
            SensorType.PRESSURE: 110,
            SensorType.TEMPERATURE: 70,
            SensorType.FLOW: 60,
            SensorType.VIBRATION: 15,
            SensorType.GAS: 5,
        }
<<<<<<< HEAD
    
    def tick(self, inject_fault: bool = False):
=======

    def tick(self, fault=None):

>>>>>>> origin/dev-ashutosh-zinia
        telemetry = []

        for sensor, value in self.sensors.items():

<<<<<<< HEAD
            # Force a pressure spike for demo purposes
            if inject_fault and sensor == SensorType.PRESSURE:
                value = 155

            else:
=======
            if (
                fault is not None
                and fault["sensor"] == sensor
            ):

                value = fault["value"]

            else:

>>>>>>> origin/dev-ashutosh-zinia
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

<<<<<<< HEAD
        return telemetry        
=======
        return telemetry
>>>>>>> origin/dev-ashutosh-zinia
