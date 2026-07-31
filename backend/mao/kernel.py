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

from services.asset import AssetService
from services.health import HealthService
from services.persistence import PersistenceService
from datetime import datetime
from mao.models.execution_report import ExecutionReport



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

        self.persistence = PersistenceService()



        # Events

        self.event_bus = EventBus()

        self.event_store = EventStore()



        # Workflow

        self.planner = Planner()

        self.workflow_engine = WorkflowEngine()

        self.supervisor = Supervisor()



        # Executor

        self.executor = Executor(
            self.registry
        )



        # Orchestrator

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

            health_service=self.health,

        )



    def register_agent(self, agent):

        self.registry.register(agent)



    def register_workflow(self, workflow):

        self.workflow_engine.register(workflow)



    def handle_event(self, event):
        try:
            report = self.orchestrator.run(event)
        except Exception as error:
            # Preserve a one-to-one incident/report audit trail even if an
            # agent or provider fails mid-workflow.
            if not any(getattr(item, "id", None) == event.id for item in self.state.events):
                self.state.add_event(event)
            report = ExecutionReport(
                execution_id=f"fallback-{event.id}",
                workflow_name="incident_fallback",
                success=False,
                started_at=getattr(event, "timestamp", datetime.now()),
                completed_at=datetime.now(),
                agent_results=[],
                final_summary=(
                    f"{event.name} was detected for asset {event.source}. "
                    "The automated investigation could not complete; operator review is required."
                ),
                recommendations=["Open the incident evidence and perform an operator-led safety review."],
                approval_required=True,
                incident_severity="Unknown",
                metadata={
                    "incident_id": event.id,
                    "incident_type": event.name,
                    "asset_id": event.source,
                    "fallback_reason": type(error).__name__,
                },
            )
            self.state.add_report(report)



        # Store report




        # Store agent outputs

        for result in report.agent_results:

            self.state.add_agent_result(result)

        self.persistence.record_execution(event, report)



        return report
