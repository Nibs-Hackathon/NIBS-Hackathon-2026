from abc import ABC, abstractmethod
from mao.models.result import AgentResult


class Agent(ABC):

    name = ""

    def think(self, task):
        print(f"[{self.name}] Thinking about '{task.name}'...")

    @abstractmethod
    def execute(self, task, context):
        pass

    def reflect(self, result):
        print(
            f"[{self.name}] Finished | "
            f"Success: {result.success} | "
            f"Confidence: {result.confidence:.2f}"
        )