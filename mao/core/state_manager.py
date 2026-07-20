from collections import defaultdict


class StateManager:

    def __init__(self):

        self.assets = {}

        # asset_id -> list[Sensor]
        self.telemetry = defaultdict(list)

        self.incidents = {}

        self.events = []

        self.execution_reports = []

        self.agent_results = []
        self.tasks = []

    # --------------------
    # Assets
    # --------------------

    def add_asset(self, asset):
        self.assets[asset.id] = asset

    def get_asset(self, asset_id):
        return self.assets.get(asset_id)

    # --------------------
    # Telemetry
    # --------------------

    def add_telemetry(self, readings):

        for reading in readings:

            history = self.telemetry[reading.asset_id]

            history.append(reading)

            if len(history) > 100:
                history.pop(0)

    def get_history(self, asset_id):

        return self.telemetry.get(asset_id, [])

    # --------------------
    # Incidents
    # --------------------

    def add_incident(self, incident):
        self.incidents[incident.id] = incident

    def active_incidents(self):

        return [
            incident
            for incident in self.incidents.values()
            if not incident.resolved
        ]

    # --------------------
    # Events
    # --------------------

    def add_event(self, event):
        self.events.append(event)

    # --------------------
    # Reports
    # --------------------

    def add_report(self, report):
        self.execution_reports.append(report)

    # --------------------
    # Agent Results
    # --------------------

    def add_agent_result(self, result):
        self.agent_results.append(result)

    # --------------------
    # Tasks
    # --------------------

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def clear_tasks(self):
        self.tasks.clear()