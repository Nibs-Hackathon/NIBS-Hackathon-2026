from agents.base import Agent
from mao.models.result import AgentResult


class PlanningAgent(Agent):

    name = "planning"

    def execute(self, task, context):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.92,
            summary="Maintenance scheduled.",
            recommendations=[
                "Assign technician",
                "Notify operations",
            ],
        )