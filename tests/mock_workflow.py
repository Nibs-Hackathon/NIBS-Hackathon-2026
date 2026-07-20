from mao.workflows.workflow import Workflow
from mao.models.task import Task


class MockWorkflow(Workflow):

    name = "default"

    def build(self, event):

        return [
            Task(
                name="Mock Task",
                description="Test task",
                assigned_agent="mock",
                priority=1,
            )
        ]