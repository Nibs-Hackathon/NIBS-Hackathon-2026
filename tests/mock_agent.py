from mao.models.result import AgentResult


class MockAgent:

    def __init__(self):
        self.name = "mock"

    def execute(self, task):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=1.0,
            summary="Mock execution successful.",
            recommendations=[],
        )