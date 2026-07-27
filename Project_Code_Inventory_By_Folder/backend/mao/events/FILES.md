# Folder: backend/mao/events Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/mao/events`

Contains 3 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/mao/events/event.py

**Folder path:** `backend/mao/events`

**File path:** `backend/mao/events/event.py`

```python
from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    source: str

    payload: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=datetime.now)
```

## backend/mao/events/event_bus.py

**Folder path:** `backend/mao/events`

**File path:** `backend/mao/events/event_bus.py`

```python
from collections import defaultdict


class EventBus:

    def __init__(self):

        self._subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):

        self._subscribers[event_name].append(callback)

    def publish(self, event):

        if event.name not in self._subscribers:
            return

        for callback in self._subscribers[event.name]:

            callback(event)
```

## backend/mao/events/event_store.py

**Folder path:** `backend/mao/events`

**File path:** `backend/mao/events/event_store.py`

```python
class EventStore:

    def __init__(self):

        self.events = []

    def save(self, event):

        self.events.append(event)

    def all(self):

        return self.events
```
