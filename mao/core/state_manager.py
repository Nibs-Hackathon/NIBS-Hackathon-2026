from collections import defaultdict


class StateManager:

    def __init__(self):

<<<<<<< HEAD
        # Assets
=======
<<<<<<< HEAD
>>>>>>> origin/dev-abeer
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
<<<<<<< HEAD
    # -------------------------
=======
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
>>>>>>> origin/dev-abeer

    def add_asset(self, asset):
        self.assets[asset.id] = asset

    def get_asset(self, asset_id):
        return self.assets.get(asset_id)

<<<<<<< HEAD
    # -------------------------
    # Telemetry
    # -------------------------
=======
<<<<<<< HEAD
    # --------------------
    # Telemetry
    # --------------------
=======
    # -------------------------
    # Telemetry
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer

    def add_telemetry(self, readings):

        for reading in readings:

            history = self.telemetry[reading.asset_id]

            history.append(reading)

            if len(history) > 100:
                history.pop(0)

    def get_history(self, asset_id):
<<<<<<< HEAD
=======
<<<<<<< HEAD

>>>>>>> origin/dev-abeer
        return self.telemetry.get(asset_id, [])

    # -------------------------
    # Events
<<<<<<< HEAD
    # -------------------------
=======
    # --------------------
=======
        return self.telemetry.get(asset_id, [])

    # -------------------------
    # Events
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer

    def add_event(self, event):
        self.events.append(event)

<<<<<<< HEAD
    # -------------------------
    # Reports
    # -------------------------
=======
<<<<<<< HEAD
    # --------------------
    # Reports
    # --------------------
=======
    # -------------------------
    # Reports
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer

    def add_report(self, report):
        self.execution_reports.append(report)

<<<<<<< HEAD
    # -------------------------
    # Agent Results
    # -------------------------
=======
<<<<<<< HEAD
    # --------------------
    # Agent Results
    # --------------------
=======
    # -------------------------
    # Agent Results
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer

    def add_agent_result(self, result):
        self.agent_results.append(result)

<<<<<<< HEAD
    # -------------------------
    # Tasks
    # -------------------------
=======
<<<<<<< HEAD
    # --------------------
    # Tasks
    # --------------------
=======
    # -------------------------
    # Tasks
    # -------------------------
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def clear_tasks(self):
<<<<<<< HEAD
=======
<<<<<<< HEAD
        self.tasks.clear()
=======
>>>>>>> origin/dev-abeer
        self.tasks.clear()

    def add_memory(self, item):
        self.memory.append(item)
    
    def get_memory(self):

        return self.memory
<<<<<<< HEAD
=======
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer
