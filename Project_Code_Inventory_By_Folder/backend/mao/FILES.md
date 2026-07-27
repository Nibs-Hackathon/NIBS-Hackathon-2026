# Folder: backend/mao Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/mao`

Contains 3 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/mao/__init__.py

**Folder path:** `backend/mao`

**File path:** `backend/mao/__init__.py`

```python
from .kernel import MAOKernel

__all__ = [
    "MAOKernel",
]
```

## backend/mao/kernel.py

**Folder path:** `backend/mao`

**File path:** `backend/mao/kernel.py`

```python
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

        # Run MAO pipeline

        report = self.orchestrator.run(event)



        # Store report




        # Store agent outputs

        for result in report.agent_results:

            self.state.add_agent_result(result)

        self.persistence.record_execution(event, report)



        return report
```

## backend/mao/orchestrator.py

**Folder path:** `backend/mao`

**File path:** `backend/mao/orchestrator.py`

```python
"""Optimized Orchestrator with parallel agent execution."""

import concurrent.futures
import time
from datetime import datetime
from mao.core.context import ExecutionContext
from mao.models.execution_report import ExecutionReport
from mao.models.task import TaskStatus


class Orchestrator:
    def __init__(
        self,
        *,
        planner,
        workflow_engine,
        scheduler,
        executor,
        supervisor,
        state_manager,
        memory_manager,
        logger,
        event_store,
        health_service=None,
    ):
        self.planner = planner
        self.workflow_engine = workflow_engine        
        self.scheduler = scheduler
        self.executor = executor
        self.supervisor = supervisor

        self.state = state_manager
        self.memory = memory_manager
        self.logger = logger
        self.event_store = event_store
        self.health_service = health_service

    def run(self, event):
        context = ExecutionContext(
            event=event,
            state_manager=self.state,
            memory_manager=self.memory,
            logger=self.logger,
            health_service=self.health_service,
        )

        self.logger.info("Kernel", f"[{context.execution_id}] Received event '{event.name}'")

        self.state.add_event(event)
        self.event_store.save(event)

        workflow_name = self.planner.choose_workflow(event)
        context.workflow = workflow_name

        self.logger.info("Planner", f"[{context.execution_id}] Selected workflow '{workflow_name}'")

        tasks = self.workflow_engine.create_tasks(workflow_name, event)

        self.logger.info("WorkflowEngine", f"[{context.execution_id}] Generated {len(tasks)} task(s)")

        # Schedule tasks
        for task in tasks:
            # Preserve operational context on every task.  Agent output and
            # maintenance planning can then be traced to the exact asset and
            # incident instead of being rendered as anonymous workflow cards.
            task.input_data = {
                **(task.input_data or {}),
                "incident_id": event.id,
                "asset_id": event.source,
                "incident_type": event.name,
                "event_payload": event.payload or {},
            }
            # State is registered before execution so the Operations Center can
            # represent pending and running MAO stages without a second engine.
            self.state.add_task(task)
            self.scheduler.submit(task)

        # ✅ Execute tasks in parallel
        def execute_task(task):
            task.status = TaskStatus.RUNNING
            result = self.executor.execute(task, context)
            context.add_result(result)
            task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
            return result

        start = time.time()
        
        # Extract all tasks first
        all_tasks = []
        while not self.scheduler.empty():
            all_tasks.append(self.scheduler.next())
        
        # Execute in parallel with ThreadPoolExecutor
        if all_tasks:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(execute_task, task): task for task in all_tasks}
                
                for future in concurrent.futures.as_completed(futures):
                    task = futures[future]
                    try:
                        result = future.result(timeout=30)
                    except Exception as e:
                        self.logger.info("Executor", f"Task {task.name} failed: {e}")

        elapsed = time.time() - start
        self.logger.info("Executor", f"[{context.execution_id}] All agents completed in {elapsed:.2f}s")

        # Aggregate results
        decision = self.supervisor.summarize(context)

        report = ExecutionReport(
            execution_id=context.execution_id,
            workflow_name=workflow_name,
            success=decision["success"],
            started_at=context.started_at,
            completed_at=datetime.now(),
            agent_results=context.results,
            final_summary=decision["summary"],
            recommendations=decision["recommendations"],
            total_agents=context.execution_metrics["agents_executed"],
            successful_agents=context.execution_metrics["successful_agents"],
            failed_agents=context.execution_metrics["failed_agents"],
            average_confidence=context.execution_metrics["average_confidence"],
            approval_required=context.requires_human_approval,
            incident_severity=context.incident_level or "Unknown",
            metadata=context.metadata,
        )

        self.state.add_report(report)
        self.memory.remember_event(event)
        self.memory.remember_report(report)

        for result in report.agent_results:
            self.memory.remember_result(result)

        return report
```
