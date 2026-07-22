class Planner:

    def choose_workflow(self, event):
<<<<<<< HEAD
=======
<<<<<<< HEAD
        return "default"
=======
>>>>>>> origin/dev-abeer

        workflows = {
            "PressureSpike": "pressure_response",
            "HighTemperature": "temperature_response",
            "GasLeak": "gas_response",
            "HighVibration": "maintenance_response",
            "FlowRestriction": "flow_response",
        }

<<<<<<< HEAD
        return workflows.get(event.name, "default")
=======
        return workflows.get(event.name, "default")
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer
