from abc import ABC, abstractmethod
from mao.result import AgentResult


class BaseAgent(ABC):

    def __init__(self, name):

        self.name = name

    def __init__(self,name):
        self.name = name
    def think(self,task):
        print(f"{self.name} thinking about '{task.name}...")
    @abstractmethod
    def execute(self, task) -> AgentResult:
        pass
    def reflect(self):
        print(f"{self.name} finished. Result")