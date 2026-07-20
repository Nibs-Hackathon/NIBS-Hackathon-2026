from mao.events.event import Event
from models.sensor import SensorType

class EventGenerator:
    def generate(self, telemetry):

        for reading in telemetry:

            if (
                reading.sensor_type == SensorType.PRESSURE and reading.value > 140
            ):
                return Event(
                    name = "PressureSpike",
                    source=reading.asset_id,
                    payload = {
                        "pressure":reading.value
                    },
                )
        return None
    
