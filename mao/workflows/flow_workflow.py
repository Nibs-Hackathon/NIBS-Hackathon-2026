from mao.workflows.workflow import Workflow
from mao.models.task import Task


class FlowWorkflow(Workflow):

    name = "flow_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Assess risks caused by restricted flow.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Flow Diagnosis",
                description="Determine the cause of flow restriction.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve flow restriction operating procedures.",
                assigned_agent="knowledge",
                priority=3,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for restricted flow.",
                assigned_agent="maintenance",
                priority=4,
            ),

            Task(
                name="Recovery Plan",
                description="Generate a flow recovery procedure.",
                assigned_agent="planning",
                priority=5,
            ),
        ]