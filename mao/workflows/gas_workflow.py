from mao.workflows.workflow import Workflow
from mao.models.task import Task


class GasWorkflow(Workflow):

    name = "gas_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Assess gas leak hazards.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Gas Leak Diagnosis",
                description="Identify the source of the gas leak.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve gas leak emergency procedures.",
                assigned_agent="knowledge",
                priority=3,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend repair actions for the gas leak.",
                assigned_agent="maintenance",
                priority=4,
            ),

            Task(
                name="Recovery Plan",
                description="Generate a gas leak recovery plan.",
                assigned_agent="planning",
                priority=5,
            ),
        ]