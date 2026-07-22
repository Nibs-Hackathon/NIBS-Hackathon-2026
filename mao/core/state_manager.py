from collections import defaultdict


class StateManager:

    def __init__(self):

<<<<<<< HEAD
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
=======
        # Assets
        self.assets = {}

        # Last 100 telemetry readings per asset
        self.telemetry = defaultdict(list)

        # Events
        self.events = []

        # Reports
        self.execution_reports = []

        # Agent Results
        self.agent_results = []

        # Workflow Tasks
        self.tasks = []
        
        # Memory
        self.memory = []

    # -------------------------
    # Assets
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia

    def add_asset(self, asset):
        self.assets[asset.id] = asset

    def get_asset(self, asset_id):
        return self.assets.get(asset_id)

<<<<<<< HEAD
    # --------------------
    # Telemetry
    # --------------------
=======
    # -------------------------
    # Telemetry
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia

    def add_telemetry(self, readings):

        for reading in readings:

            history = self.telemetry[reading.asset_id]

            history.append(reading)

            if len(history) > 100:
                history.pop(0)

    def get_history(self, asset_id):
<<<<<<< HEAD

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
=======
        return self.telemetry.get(asset_id, [])

    # -------------------------
    # Events
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia

    def add_event(self, event):
        self.events.append(event)

<<<<<<< HEAD
    # --------------------
    # Reports
    # --------------------
=======
    # -------------------------
    # Reports
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia

    def add_report(self, report):
        self.execution_reports.append(report)

<<<<<<< HEAD
    # --------------------
    # Agent Results
    # --------------------
=======
    # -------------------------
    # Agent Results
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia

    def add_agent_result(self, result):
        self.agent_results.append(result)

<<<<<<< HEAD
    # --------------------
    # Tasks
    # --------------------
=======
    # -------------------------
    # Tasks
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def clear_tasks(self):
<<<<<<< HEAD
        self.tasks.clear()
=======
        self.tasks.clear()

    def add_memory(self, item):
        self.memory.append(item)
    
    def get_memory(self):

        return self.memory
>>>>>>> origin/dev-ashutosh-zinia
