
from models.sensor import SensorType


class HealthService:

    LIMITS = {
        SensorType.PRESSURE: 150,
        SensorType.TEMPERATURE: 90,
        SensorType.FLOW: 40,
        SensorType.VIBRATION: 25,
        SensorType.GAS: 15,
    }

    def calculate_health(self, readings):

        score = 100

        for reading in readings:

            limit = self.LIMITS.get(reading.sensor_type)

            if limit is None:
                continue

            if reading.value > limit:

                excess = reading.value - limit

                score -= excess * 2

        return max(score, 0)