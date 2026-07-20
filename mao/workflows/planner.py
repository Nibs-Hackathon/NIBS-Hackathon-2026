from mao.models.task import Task


class Planner:

    def choose_workflow(self, event):

        match event.name:

            case "PressureSpike":
                return "pressure_spike"

            case "GasLeak":
                return "gas_leak"

            case _:
                return "default"