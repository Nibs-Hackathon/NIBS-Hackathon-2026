from datetime import datetime
from uuid import uuid4


class ExecutionContext:

    def __init__(
        self,
        event,
        state_manager,
        memory_manager,
        logger,
    ):

        self.execution_id = str(uuid4())

        self.started_at = datetime.now()

        self.event = event

        self.workflow = None

        self.state = state_manager

        self.memory = memory_manager

        self.logger = logger

        self.results = []

        self.metadata = {}