"""Mock workflow for testing purposes."""

from mao.workflows.workflow import Workflow
from mao.models.task import Task


class MockWorkflow(Workflow):
    """A simple mock workflow for testing the MAO system."""

    name = "mock_workflow"

    def build(self, event):
        """Create a single task for testing."""
        return [
            Task(
                name="Mock Task",
                description="Mock task for testing",
                assigned_agent="safety",
                priority=1,
                input_data={
                    "event_id": event.id,
                    "event_name": event.name,
                    "source": event.source,
                }
            )
        ]