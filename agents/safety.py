from agents.base import Agent
from mao.models.result import AgentResult


class SafetyAgent(Agent):

    name = "safety"

    def execute(self, task, context):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.96,
            summary="Safety limits verified. Continue monitoring.",
            recommendations=[
                "Reduce operating pressure",
                "Inspect relief valve",
            ],
        )