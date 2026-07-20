from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, name):

        self.name = name

    def __init__(self,name):
        self.name = name
    def think(self,task):
        print(f"{self.name} thinking...")
    @abstractmethod
    def execute(self, task):
        pass
    def reflect(self):
        print(f"{self.name} finished.")