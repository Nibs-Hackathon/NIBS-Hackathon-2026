from agents.base import Agent
from mao.models.result import AgentResult


class DiagnosticAgent(Agent):

    name = "diagnostic"

    def execute(self, task, context):

        return AgentResult(

            agent_name=self.name,

            success=True,

            finding=
            "Possible cavitation detected in pump system",

            confidence=0.95,


            evidence=[
                "Abnormal vibration pattern",
                "Reduced suction pressure"
            ],


            recommendations=[
                "Inspect pump inlet",
                "Check suction pressure"
            ],


            required_action=
            "Perform pump inspection",


            requires_human_approval=True

        )