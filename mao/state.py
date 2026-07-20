from typing import Any

from mao.event import Event
from mao.task import Task


class GlobalState:

    def __init__(self):
        self.facilities = {}
        self.assets = {}
        self.incidents = {}
        self.tasks: dict[str, Task] = {}
        self.events: list[Event] = []
        self.shared_memory: dict[str, Any] = {}

    def add_event(self, event: Event):
        self.events.append(event)

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def get_memory(self, key: str):
        return self.shared_memory.get(key)

    def set_memory(self, key: str, value):
        self.shared_memory[key] = value
