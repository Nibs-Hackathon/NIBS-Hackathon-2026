from agents.base_agent import BaseAgent
from mao.result import AgentResult

class SafetyAgent(BaseAgent):

    def __init__(self):

        super().__init__("SafetyAgent")

    def execute(self, task):

        self.think(task)
        pressure = task.input_data.get("pressure, 0")

        if pressure >110:
            risk = "HIGH"
            reccommendations = [
                "Close isolation valve",
                "Alert field operators",
                "Reduce line pressure"
            ]
            confidence = 0.97
        else:
            risk = "LOW"
            reccommendations = ["Continue monitoring"]
            confidence = 0.85
        return AgentResult(
            agent_name=self.name,
            confidence=confidence,
            summary = f"Saftey assesment: {risk}",
            reccomendations = reccommendations,
            metadata = {
                "risk":risk,
                "pressure": pressure,
            },

        )
       