from mao.workflows.workflow import Workflow
from mao.models.task import Task


class TemperatureWorkflow(Workflow):

    name = "temperature_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Evaluate overheating risks.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Temperature Diagnosis",
                description="Determine the cause of abnormal temperature.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for overheating equipment.",
                assigned_agent="maintenance",
                priority=3,
            ),

            Task(
                name="Recovery Plan",
                description="Create a safe recovery procedure.",
                assigned_agent="planning",
                priority=4,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve overheating operating procedures.",
                assigned_agent="knowledge",
                priority=5,
            ),
        ]
