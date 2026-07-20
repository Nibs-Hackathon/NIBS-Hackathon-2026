from mao.task import Task


class Planner:

    def create_plan(self, event):

        tasks = []

        if event.name == "PressureSpike":

            tasks.append(
                Task(
                    name="Safety Check",
                    description="Evaluate risk",

                    assigned_agent="SafetyAgent",

                    input_data=event.payload,
                )
            )

            tasks.append(
                Task(
                    name="Inspect Pump",

                    description="Check pump integrity",

                    assigned_agent="MaintenanceAgent",

                    input_data=event.payload,
                )
            )

        return tasks