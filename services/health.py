<<<<<<< HEAD

=======
>>>>>>> origin/dev-ashutosh-zinia
from models.sensor import SensorType


class HealthService:
<<<<<<< HEAD
=======
    """
    Calculates asset health from recent telemetry.
    """
>>>>>>> origin/dev-ashutosh-zinia

    LIMITS = {
        SensorType.PRESSURE: 150,
        SensorType.TEMPERATURE: 90,
        SensorType.FLOW: 40,
        SensorType.VIBRATION: 25,
        SensorType.GAS: 15,
    }

    def calculate_health(self, readings):

<<<<<<< HEAD
        score = 100
=======
        health = 100.0
>>>>>>> origin/dev-ashutosh-zinia

        for reading in readings:

            limit = self.LIMITS.get(reading.sensor_type)

            if limit is None:
                continue

<<<<<<< HEAD
            if reading.value > limit:

                excess = reading.value - limit

                score -= excess * 2

        return max(score, 0)
=======
            if reading.sensor_type == SensorType.FLOW:

                if reading.value < limit:
                    health -= 5

            else:

                if reading.value > limit:
                    health -= 5

        return max(0.0, health)
>>>>>>> origin/dev-ashutosh-zinia
