from agents.base import Agent
from mao.models.result import AgentResult


class DiagnosticAgent(Agent):

    name = "diagnostic"

    def execute(self, task, context):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.95,
            summary="Possible cavitation detected.",
            recommendations=[
                "Inspect pump inlet",
                "Check suction pressure",
            ],
        )