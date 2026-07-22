from mao.core.executor import Executor
from mao.core.logger import KernelLogger
from mao.core.registry import AgentRegistry
from mao.core.scheduler import Scheduler
from mao.core.state_manager import StateManager

from mao.events.event_bus import EventBus
from mao.events.event_store import EventStore

from mao.memory.memory_manager import MemoryManager

from mao.orchestrator import Orchestrator

from mao.workflows.planner import Planner
from mao.workflows.supervisor import Supervisor
from mao.workflows.workflow_engine import WorkflowEngine
<<<<<<< HEAD

=======
<<<<<<< HEAD
from services.health import HealthService
>>>>>>> origin/dev-abeer
from services.asset import AssetService
from services.health import HealthService


class MAOKernel:

    def __init__(self):

        # Core
        self.registry = AgentRegistry()
        self.scheduler = Scheduler()
        self.state = StateManager()
        self.logger = KernelLogger()
        self.memory = MemoryManager()

        # Services
        self.asset_service = AssetService()
        self.health = HealthService()

        # Events
        self.event_bus = EventBus()
        self.event_store = EventStore()

        # Workflow
        self.planner = Planner()
        self.workflow_engine = WorkflowEngine()
        self.supervisor = Supervisor()

        # Executor
        self.executor = Executor(self.registry)

<<<<<<< HEAD
        # Orchestrator
=======
        # ---------------- Orchestrator ----------------

=======

from services.asset import AssetService
from services.health import HealthService


class MAOKernel:

    def __init__(self):

        # Core
        self.registry = AgentRegistry()
        self.scheduler = Scheduler()
        self.state = StateManager()
        self.logger = KernelLogger()
        self.memory = MemoryManager()

        # Services
        self.asset_service = AssetService()
        self.health = HealthService()

        # Events
        self.event_bus = EventBus()
        self.event_store = EventStore()

        # Workflow
        self.planner = Planner()
        self.workflow_engine = WorkflowEngine()
        self.supervisor = Supervisor()

        # Executor
        self.executor = Executor(self.registry)

        # Orchestrator
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer
        self.orchestrator = Orchestrator(
            planner=self.planner,
            workflow_engine=self.workflow_engine,
            scheduler=self.scheduler,
            executor=self.executor,
            supervisor=self.supervisor,
            state_manager=self.state,
            memory_manager=self.memory,
            logger=self.logger,
            event_store=self.event_store,
        )

<<<<<<< HEAD
=======
<<<<<<< HEAD
    # -------------------------------------------------

>>>>>>> origin/dev-abeer
    def register_agent(self, agent):
        self.registry.register(agent)

    def register_workflow(self, workflow):
<<<<<<< HEAD
=======

=======
    def register_agent(self, agent):
        self.registry.register(agent)

    def register_workflow(self, workflow):
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer
        self.workflow_engine.register(workflow)

    def handle_event(self, event):

<<<<<<< HEAD
=======
<<<<<<< HEAD
        # Store the incoming event
        self.state.add_event(event)

        # Run the MAO pipeline
>>>>>>> origin/dev-abeer
        report = self.orchestrator.run(event)

        self.state.add_report(report)

<<<<<<< HEAD
=======
        # Store every agent result
=======
        report = self.orchestrator.run(event)

        self.state.add_report(report)

>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer
        for result in report.agent_results:
            self.state.add_agent_result(result)

        return report