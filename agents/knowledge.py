from agents.base import Agent
from mao.models.result import AgentResult


class KnowledgeAgent(Agent):

    name = "knowledge"

    def execute(self, task, context):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.92,
            summary="Relevant SOP retrieved.",
            recommendations=[
                "Follow Pressure SOP Section 4",
                "Notify control room",
            ],
        )