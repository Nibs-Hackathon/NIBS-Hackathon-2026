from mao.workflows.workflow import Workflow
from mao.models.task import Task


class PressureWorkflow(Workflow):

    name = "pressure_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Analyze safety impact of the pressure spike.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Root Cause Analysis",
                description="Determine the likely cause of the pressure spike.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for the affected equipment.",
                assigned_agent="maintenance",
                priority=3,
            ),

            Task(
                name="Recovery Plan",
                description="Generate the recovery and restart plan.",
                assigned_agent="planning",
                priority=4,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve the pressure spike operating procedure.",
                assigned_agent="knowledge",
                priority=5,
            ),
        ]
