from agents.base import Agent
from mao.models.result import AgentResult


class MockAgent(Agent):

    def __init__(self):

        super().__init__("mock")


    def execute(self, task):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=1.0,
            summary="Mock execution successful.",
            recommendations=[],
            metadata={},
            execution_time=0.0,
        )