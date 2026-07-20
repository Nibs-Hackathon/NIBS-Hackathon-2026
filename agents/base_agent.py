from abc import ABC, abstractmethod

from mao.models.task import Task
from mao.models.result import AgentResult


class BaseAgent(ABC):
    """
    Base class for all MAO agents.
    """

    def __init__(self, name: str):
        self.name = name

    def think(self, task: Task) -> None:
        print(f"[{self.name}] Thinking about '{task.name}'...")

    @abstractmethod
    def execute(self, task: Task) -> AgentResult:
        """
        Execute a task and return an AgentResult.
        """
        pass

    def reflect(self, result: AgentResult) -> None:
        print(
            f"[{self.name}] Finished | "
            f"Success: {result.success} | "
            f"Confidence: {result.confidence:.2f}"
        )