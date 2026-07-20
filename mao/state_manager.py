from typing import Any

from mao.event import Event
from mao.task import Task


class StateManager:

    def __init__(self):

        self.events: list[Event] = []

        self.tasks: dict[str, Task] = {}

        self.assets = {}

        self.facilities = {}

        self.incidents = {}

        self.shared_memory: dict[str, Any] = {}

    def add_event(self, event):

        self.events.append(event)

    def add_task(self, task):

        self.tasks[task.id] = task

    def update_task(self, task):

        self.tasks[task.id] = task

    def latest_events(self, n=10):

        return self.events[-n:]