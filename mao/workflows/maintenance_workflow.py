from mao.workflows.workflow import Workflow
from mao.models.task import Task


class MaintenanceWorkflow(Workflow):

    name = "maintenance_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Verify equipment is safe before maintenance.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Equipment Diagnosis",
                description="Analyze equipment condition.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Maintenance Planning",
                description="Generate maintenance recommendations.",
                assigned_agent="maintenance",
                priority=3,
            ),

            Task(
                name="Execution Plan",
                description="Create the maintenance execution plan.",
                assigned_agent="planning",
                priority=4,
            ),

            Task(
                name="Retrieve Manual",
                description="Retrieve maintenance manuals and procedures.",
                assigned_agent="knowledge",
                priority=5,
            ),
        ]
