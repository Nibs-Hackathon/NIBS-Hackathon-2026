from agents.base_agent import BaseAgent


class SafetyAgent(BaseAgent):

    def __init__(self):

        super().__init__("SafetyAgent")

    def execute(self, task):

        self.think(task)
        print()
        print("Running safety analysis...")
        print(task.input_data)

        task.output_data = {
            "risk":"HIGH",
            "action": "Evacuate Area",
        }
        task.status = "COMPLETED"
        self.reflect()
        return task