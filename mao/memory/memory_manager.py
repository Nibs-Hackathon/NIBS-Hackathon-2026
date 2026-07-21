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