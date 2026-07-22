from mao.events.event import Event
from models.sensor import SensorType

<<<<<<< HEAD
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
    
=======

class EventGenerator:

    def generate(self, telemetry):

        events = []

        for reading in telemetry:

            # Pressure
            if (
                reading.sensor_type == SensorType.PRESSURE
                and reading.value > 140
            ):
                events.append(
                    Event(
                        name="PressureSpike",
                        source=reading.asset_id,
                        payload={
                            "pressure": reading.value,
                        },
                    )
                )

            # Temperature
            elif (
                reading.sensor_type == SensorType.TEMPERATURE
                and reading.value > 90
            ):
                events.append(
                    Event(
                        name="HighTemperature",
                        source=reading.asset_id,
                        payload={
                            "temperature": reading.value,
                        },
                    )
                )

            # Gas
            elif (
                reading.sensor_type == SensorType.GAS
                and reading.value > 25
            ):
                events.append(
                    Event(
                        name="GasLeak",
                        source=reading.asset_id,
                        payload={
                            "gas": reading.value,
                        },
                    )
                )

            # Vibration
            elif (
                reading.sensor_type == SensorType.VIBRATION
                and reading.value > 30
            ):
                events.append(
                    Event(
                        name="HighVibration",
                        source=reading.asset_id,
                        payload={
                            "vibration": reading.value,
                        },
                    )
                )

            # Flow
            elif (
                reading.sensor_type == SensorType.FLOW
                and reading.value < 25
            ):
                events.append(
                    Event(
                        name="FlowRestriction",
                        source=reading.asset_id,
                        payload={
                            "flow": reading.value,
                        },
                    )
                )

        return events
>>>>>>> origin/dev-ashutosh-zinia
