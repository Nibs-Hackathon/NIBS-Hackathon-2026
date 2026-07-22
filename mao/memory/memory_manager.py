<<<<<<< HEAD
=======
<<<<<<< HEAD
from typing import Any


>>>>>>> origin/dev-abeer
class MemoryManager:

    def __init__(self):

        self.execution_reports = []

        self.agent_results = []

        self.events = []

    # -------------------------

    def remember_report(self, report):

<<<<<<< HEAD
=======
    def all(self) -> dict[str, Any]:
        """Return the full memory dictionary."""
        return self._memory.copy()
=======
class MemoryManager:

    def __init__(self):

        self.execution_reports = []

        self.agent_results = []

        self.events = []

    # -------------------------

    def remember_report(self, report):

>>>>>>> origin/dev-abeer
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

<<<<<<< HEAD
        return self.execution_reports[-1]
=======
        return self.execution_reports[-1]
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer
