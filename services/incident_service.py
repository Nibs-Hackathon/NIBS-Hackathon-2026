
from models.sensor import SensorType


class IncidentService:

    def __init__(self, simulator):

        self.simulator = simulator


    def trigger_incident(self, incident_type):

        fault = None


        if incident_type == "Pressure Spike":

            fault = {
                "sensor": SensorType.PRESSURE,
                "value": 155
            }


        elif incident_type == "Gas Leak":

            fault = {
                "sensor": SensorType.GAS,
                "value": 30
            }


        elif incident_type == "High Vibration":

            fault = {
                "sensor": SensorType.VIBRATION,
                "value": 40
            }



        telemetry, reports = self.simulator.tick(
            tick_number=1,
            fault=fault
        )


        return {
            "telemetry": telemetry,
            "reports": reports
        }