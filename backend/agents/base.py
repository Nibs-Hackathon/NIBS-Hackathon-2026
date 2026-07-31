from abc import ABC, abstractmethod

from mao.models.result import AgentResult


class Agent(ABC):

    name = ""

    def think(self, task):
        print(
            f"[{self.name}] analyzing '{task.name}'"
        )

    @abstractmethod
    def execute(self, task, context) -> AgentResult:
        """
        Every agent must return an AgentResult.
        """
        pass

    def validate_result(self, result: AgentResult):

        if not isinstance(result, AgentResult):
            raise TypeError(
                f"{self.name} must return AgentResult."
            )

        required_fields = [
            "finding",
            "confidence",
            "recommendations",
            "success",
            "summary",
        ]

        for field in required_fields:

            if not hasattr(result, field):
                raise ValueError(
                    f"{self.name}: Missing field '{field}'"
                )

        if not 0 <= result.confidence <= 1:
            raise ValueError(
                f"{self.name}: Confidence must be between 0 and 1."
            )

        return True

    def reflect(self, result: AgentResult):

        print(
            f"""
==============================
Agent: {self.name}
==============================

Finding:
{result.finding}

Confidence:
{result.confidence:.2f}

Recommendations:
{len(result.recommendations)}

Evidence:
{len(result.evidence)}

Requires Approval:
{result.requires_human_approval}

Summary:
{result.summary}

==============================
"""
        )

    def run(self, task, context):

        self.think(task)

        result = self.execute(
            task,
            context,
        )

        self.validate_result(result)

        self.reflect(result)

        return result