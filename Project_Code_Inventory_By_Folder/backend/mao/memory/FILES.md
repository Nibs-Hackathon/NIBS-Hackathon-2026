# Folder: backend/mao/memory Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/mao/memory`

Contains 1 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/mao/memory/memory_manager.py

**Folder path:** `backend/mao/memory`

**File path:** `backend/mao/memory/memory_manager.py`

```python

from typing import Any


class MemoryManager:

    def __init__(self):

        self.execution_reports = []

        self.agent_results = []

        self.events = []


    # -------------------------

    def remember_report(self, report):

        self.execution_reports.append(report)



    # -------------------------

    def remember_result(self, result):

        self.agent_results.append(result)



    # -------------------------

    def remember_event(self, event):

        self.events.append(event)



    # -------------------------

    def latest_report(self):

        if not self.execution_reports:

            return None


        return self.execution_reports[-1]
```
