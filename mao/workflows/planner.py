class Planner:

    def choose_workflow(self, event):
<<<<<<< HEAD
        return "default"
=======

        workflows = {
            "PressureSpike": "pressure_response",
            "HighTemperature": "temperature_response",
            "GasLeak": "gas_response",
            "HighVibration": "maintenance_response",
            "FlowRestriction": "flow_response",
        }

        return workflows.get(event.name, "default")
>>>>>>> origin/dev-ashutosh-zinia
