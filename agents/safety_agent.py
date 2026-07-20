from agents.base_agent import BaseAgent


class SafetyAgent(BaseAgent):

    def __init__(self):

        super().__init__("SafetyAgent")

    def execute(self, event):

        print()

        print(f"[Safety] Handling {event.name}")

        print(event.payload)