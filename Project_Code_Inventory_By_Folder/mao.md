# Folder: mao Code Inventory

Generated: 2026-07-24T03:28:50 UTC

Contains 30 project files.

## mao/__init__.py

**File path:** `mao/__init__.py`

```python
from .kernel import MAOKernel

__all__ = [
    "MAOKernel",
]
```

## mao/core/context.py

**File path:** `mao/core/context.py`

```python
from datetime import datetime
from uuid import uuid4
from typing import Any, Dict, List, Optional


class ExecutionContext:

    def __init__(
        self,
        event,
        state_manager,
        memory_manager,
        logger,
        health_service=None,
    ):

        # Unique execution information
        self.execution_id = str(uuid4())
        self.started_at = datetime.now()

        # Event information
        self.event = event
        self.workflow = None

        # Shared services
        self.state = state_manager
        self.memory = memory_manager
        self.logger = logger
        self.health_service = health_service

        # Agent execution
        self.results: List[Any] = []
        self.last_result: Optional[Any] = None

        # Shared knowledge between agents
        self.shared_evidence: List[str] = []
        self.shared_recommendations: List[str] = []

        # Incident state
        self.incident_level: Optional[str] = None
        self.requires_shutdown: bool = False
        self.requires_human_approval: bool = False

        # Runtime metrics
        self.execution_metrics: Dict[str, Any] = {
            "agents_executed": 0,
            "successful_agents": 0,
            "failed_agents": 0,
            "average_confidence": 0.0,
        }

        # Flexible storage for workflows/agents
        self.metadata: Dict[str, Any] = {}

    def add_result(self, result):
        """
        Register an agent result and update execution state.
        """

        self.results.append(result)
        self.last_result = result

        if result.evidence:
            self.shared_evidence.extend(result.evidence)

        if result.recommendations:
            self.shared_recommendations.extend(result.recommendations)

        self.execution_metrics["agents_executed"] += 1

        if result.success:
            self.execution_metrics["successful_agents"] += 1
        else:
            self.execution_metrics["failed_agents"] += 1

        if result.requires_human_approval:
            self.requires_human_approval = True

        if self.results:
            total = sum(r.confidence for r in self.results)
            self.execution_metrics["average_confidence"] = round(
                total / len(self.results),
                2,
            )
```

## mao/core/exceptions.py

**File path:** `mao/core/exceptions.py`

```python
class MAOException(Exception):
    """Base exception for the MAO Kernel."""


class AgentNotFound(MAOException):
    pass


class WorkflowNotFound(MAOException):
    pass


class ToolNotFound(MAOException):
    pass


class PolicyViolation(MAOException):
    pass


class TaskExecutionFailed(MAOException):
    pass
```

## mao/core/executor.py

**File path:** `mao/core/executor.py`

```python
from mao.models.result import AgentResult
from mao.core.exceptions import AgentNotFound


class Executor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, task, context):

        agent = self.registry.get(
            task.assigned_agent
        )

        if agent is None:
            raise AgentNotFound(
                f"Agent '{task.assigned_agent}' not found."
            )

        try:

            # Agent.run() handles:
            # think()
            # execute()
            # validate_result()
            # reflect()
            result = agent.run(
                task,
                context,
            )

        except Exception as e:

            result = AgentResult(
                agent_name=agent.name,
                success=False,
                finding="Agent execution failed.",
                confidence=0.0,
                summary=str(e),
                recommendations=[
                    "Review execution logs."
                ],
                metadata={
                    "exception": type(e).__name__,
                },
            )

        result.metadata.update(
            {
                "task_name": task.name,
                "task_description": task.description,
                "event_name": context.event.name,
                "asset_id": context.event.source,
            }
        )

        return result
```

## mao/core/logger.py

**File path:** `mao/core/logger.py`

```python
from datetime import datetime


class KernelLogger:

    def __init__(self):

        self.logs = []

    def info(self, source, message):

        self.logs.append(
            {
                "time": datetime.now(),

                "source": source,

                "message": message,
            }
        )

        print(f"[{source}] {message}")
```

## mao/core/registry.py

**File path:** `mao/core/registry.py`

```python
from typing import Dict


class AgentRegistry:
    """
    Stores every registered agent.
    """

    def __init__(self):

        self._agents: Dict[str, object] = {}

    def register(self, agent):

        self._agents[agent.name] = agent

    def get(self, name):

        return self._agents.get(name)

    def remove(self, name):

        self._agents.pop(name, None)

    def all(self):

        return list(self._agents.values())

    def exists(self, name):

        return name in self._agents
```

## mao/core/scheduler.py

**File path:** `mao/core/scheduler.py`

```python
import heapq

from itertools import count


class Scheduler:

    def __init__(self):

        self._queue = []

        self._counter = count()

    def submit(self, task):

        heapq.heappush(
            self._queue,

            (task.priority,

             next(self._counter),

             task)
        )

    def next(self):

        if not self._queue:

            return None

        return heapq.heappop(self._queue)[2]

    def empty(self):

        return len(self._queue) == 0
```

## mao/core/state_manager.py

**File path:** `mao/core/state_manager.py`

```python
from collections import defaultdict


class StateManager:

    def __init__(self):

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

        # Runtime Notifications
        self.notifications = []

        # Memory
        self.memory = []


    # -------------------------
    # Assets
    # -------------------------

    def add_asset(self, asset):

        self.assets[asset.id] = asset


    def get_asset(self, asset_id):

        return self.assets.get(asset_id)



    # -------------------------
    # Telemetry
    # -------------------------

    def add_telemetry(self, readings):

        for reading in readings:

            history = self.telemetry[reading.asset_id]

            history.append(reading)

            if len(history) > 100:

                history.pop(0)



    def get_history(self, asset_id):

        return self.telemetry.get(asset_id, [])



    # -------------------------
    # Events
    # -------------------------

    def add_event(self, event):

        self.events.append(event)



    # -------------------------
    # Reports
    # -------------------------

    def add_report(self, report):

        self.execution_reports.append(report)



    # -------------------------
    # Agent Results
    # -------------------------

    def add_agent_result(self, result):

        self.agent_results.append(result)



    # -------------------------
    # Tasks
    # -------------------------

    def add_task(self, task):

        self.tasks.append(task)


    def get_tasks(self):

        return self.tasks


    def clear_tasks(self):

        self.tasks.clear()


    # -------------------------
    # Notifications
    # -------------------------

    def add_notification(self, notification):

        self.notifications.append(notification)

        if len(self.notifications) > 200:

            self.notifications.pop(0)


    def get_notifications(self):

        return self.notifications



    # -------------------------
    # Memory
    # -------------------------

    def add_memory(self, item):

        self.memory.append(item)


    def get_memory(self):

        return self.memory
```

## mao/events/event_bus.py

**File path:** `mao/events/event_bus.py`

```python
from collections import defaultdict


class EventBus:

    def __init__(self):

        self._subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):

        self._subscribers[event_name].append(callback)

    def publish(self, event):

        if event.name not in self._subscribers:
            return

        for callback in self._subscribers[event.name]:

            callback(event)
```

## mao/events/event_store.py

**File path:** `mao/events/event_store.py`

```python
class EventStore:

    def __init__(self):

        self.events = []

    def save(self, event):

        self.events.append(event)

    def all(self):

        return self.events
```

## mao/events/event.py

**File path:** `mao/events/event.py`

```python
from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    source: str

    payload: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=datetime.now)
```

## mao/kernel.py

**File path:** `mao/kernel.py`

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

## mao/memory/memory_manager.py

**File path:** `mao/memory/memory_manager.py`

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

## mao/models/execution_report.py

**File path:** `mao/models/execution_report.py`

```python
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from mao.models.result import AgentResult


class ExecutionReport(BaseModel):

    # Report identifiers
    id: str = Field(default_factory=lambda: str(uuid4()))
    execution_id: str

    # Workflow information
    workflow_name: str
    success: bool

    # Timing
    started_at: datetime
    completed_at: datetime

    # Agent outputs
    agent_results: list[AgentResult]

    # Final decision
    final_summary: str
    recommendations: list[str] = Field(default_factory=list)

    # Execution metrics
    total_agents: int = 0
    successful_agents: int = 0
    failed_agents: int = 0
    average_confidence: float = 0.0

    # Approval & Incident
    approval_required: bool = False
    incident_severity: str = "Unknown"

    # Optional metadata
    metadata: dict = Field(default_factory=dict)
```

## mao/models/notification.py

**File path:** `mao/models/notification.py`

```python
"""Runtime-only notification model for MAO workflow outputs."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Notification:
    """A structured operator notification held in StateManager memory."""

    source: str
    severity: str
    summary: str
    asset_id: str | None = None
    requires_human_approval: bool = False
    metadata: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
```

## mao/models/result.py

**File path:** `mao/models/result.py`

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import uuid4


@dataclass
class AgentResult:

    agent_name: str

    success: bool

    id: str = field(default_factory=lambda: str(uuid4()))

    finding: str = ""

    confidence: float = 0.0

    evidence: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    required_action: str = ""

    requires_human_approval: bool = True

    metadata: Dict = field(default_factory=dict)

    summary: str = ""

    decision: str = ""

    actions_required: List[str] = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.now)
```

## mao/models/task.py

**File path:** `mao/models/task.py`

```python
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    description: str

    assigned_agent: str

    priority: int = 1

    status: TaskStatus = TaskStatus.PENDING

    input_data: dict = Field(default_factory=dict)

    output_data: dict = Field(default_factory=dict)
```

## mao/orchestrator.py

**File path:** `mao/orchestrator.py`

```python
from datetime import datetime

from mao.core.context import ExecutionContext
from mao.models.execution_report import ExecutionReport


class Orchestrator:
    """
    Coordinates the complete execution lifecycle for a single event.
    """

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

        self.logger.info(
            "Kernel",
            f"[{context.execution_id}] Received event '{event.name}'",
        )

        # Persist incoming event
        self.state.add_event(event)
        self.event_store.save(event)

        # Select workflow
        workflow_name = self.planner.choose_workflow(event)
        context.workflow = workflow_name

        self.logger.info(
            "Planner",
            f"[{context.execution_id}] Selected workflow '{workflow_name}'",
        )

        # Build workflow tasks
        tasks = self.workflow_engine.create_tasks(
            workflow_name,
            event,
        )

        self.logger.info(
            "WorkflowEngine",
            f"[{context.execution_id}] Generated {len(tasks)} task(s)",
        )

        # Schedule tasks
        for task in tasks:
            self.scheduler.submit(task)

        # Execute tasks
        while not self.scheduler.empty():

            task = self.scheduler.next()

            self.logger.info(
                "Executor",
                f"[{context.execution_id}] Executing '{task.name}'",
            )

            result = self.executor.execute(
                task,
                context,
            )

            # NEW
            context.add_result(result)

            self.state.add_task(task)

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

        self.logger.info(
            "Kernel",
            f"[{context.execution_id}] Execution completed.",
        )

        # Persist into memory
        self.memory.remember_event(event)
        self.memory.remember_report(report)

        for result in report.agent_results:
            self.memory.remember_result(result)

        return report
```

## mao/tools/tool_registry.py

**File path:** `mao/tools/tool_registry.py`

```python

```

## mao/workflows/flow_workflow.py

**File path:** `mao/workflows/flow_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class FlowWorkflow(Workflow):

    name = "flow_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Assess risks caused by restricted flow.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Flow Diagnosis",
                description="Determine the cause of flow restriction.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve flow restriction operating procedures.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for restricted flow.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Recovery Plan",
                description="Generate a flow recovery procedure.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## mao/workflows/gas_workflow.py

**File path:** `mao/workflows/gas_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class GasWorkflow(Workflow):

    name = "gas_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Assess gas leak hazards.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Gas Leak Diagnosis",
                description="Identify the source of the gas leak.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve gas leak emergency procedures.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend repair actions for the gas leak.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Recovery Plan",
                description="Generate a gas leak recovery plan.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## mao/workflows/intelligence_tasks.py

**File path:** `mao/workflows/intelligence_tasks.py`

```python
"""Reusable intelligence stages appended to established operational workflows."""

from mao.models.task import Task


def intelligence_tasks() -> tuple[Task, Task, Task, Task]:
    """Return the common MAO intelligence stages with stable priorities."""
    return (
        Task(
            name="Sensor Observation",
            description="Record telemetry anomaly metadata without generating events.",
            assigned_agent="sensor",
            priority=1,
        ),
        Task(
            name="Failure Risk Prediction",
            description="Estimate deterministic health, failure probability, and RUL.",
            assigned_agent="prediction",
            priority=7,
        ),
        Task(
            name="Operator Notification",
            description="Create structured runtime notifications when escalation is needed.",
            assigned_agent="notification",
            priority=8,
        ),
        Task(
            name="Report Compilation",
            description="Compile agent outputs for the existing execution report.",
            assigned_agent="report",
            priority=9,
        ),
    )
```

## mao/workflows/maintenance_workflow.py

**File path:** `mao/workflows/maintenance_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class MaintenanceWorkflow(Workflow):

    name = "maintenance_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Verify equipment is safe before maintenance.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Equipment Diagnosis",
                description="Analyze equipment condition.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve Manual",
                description="Retrieve maintenance manuals and procedures.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Planning",
                description="Generate maintenance recommendations.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Execution Plan",
                description="Create the maintenance execution plan.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## mao/workflows/planner.py

**File path:** `mao/workflows/planner.py`

```python
"""
mao/workflows/planner.py

Workflow Planner

Determines which workflow should execute based on the
incoming event and telemetry payload.

Supports both:
    • Explicit event names
    • Automatic telemetry-based routing
"""

from __future__ import annotations

from typing import Any


class Planner:
    """
    Selects the most appropriate workflow for an incoming event.
    """

    EVENT_MAP = {
        "PressureSpike": "pressure_response",
        "HighTemperature": "temperature_response",
        "GasLeak": "gas_response",
        "HighVibration": "maintenance_response",
        "FlowRestriction": "flow_response",
    }

    def choose_workflow(self, event: Any) -> str:
        """
        Determine which workflow should handle an event.

        Priority:
            1. Telemetry inspection
            2. Event-name lookup
            3. Default workflow
        """

        payload = getattr(event, "payload", {}) or {}

        workflow = self._workflow_from_payload(payload)

        if workflow is not None:
            return workflow

        return self.EVENT_MAP.get(
            getattr(event, "name", ""),
            "default",
        )

    def _workflow_from_payload(
        self,
        payload: dict,
    ) -> str | None:
        """
        Infer workflow directly from telemetry.
        """

        pressure = payload.get("pressure")
        temperature = payload.get("temperature")
        gas = payload.get("gas_level")
        vibration = payload.get("vibration")
        flow = payload.get("flow_rate")

        if pressure is not None and pressure >= 150:
            return "pressure_response"

        if temperature is not None and temperature >= 85:
            return "temperature_response"

        if gas is not None and gas >= 40:
            return "gas_response"

        if vibration is not None and vibration >= 8:
            return "maintenance_response"

        if flow is not None and flow <= 25:
            return "flow_response"

        return None
```

## mao/workflows/policy_engine.py

**File path:** `mao/workflows/policy_engine.py`

```python

```

## mao/workflows/pressure_workflow.py

**File path:** `mao/workflows/pressure_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class PressureWorkflow(Workflow):

    name = "pressure_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Analyze safety impact of the pressure spike.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Root Cause Analysis",
                description="Determine the likely cause of the pressure spike.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve the pressure spike operating procedure.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for the affected equipment.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Recovery Plan",
                description="Generate the recovery and restart plan.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## mao/workflows/supervisor.py

**File path:** `mao/workflows/supervisor.py`

```python
from collections import OrderedDict

from mao.core.context import ExecutionContext


class Supervisor:
    """
    Aggregates all agent outputs into a final execution decision.
    """

    def summarize(self, context: ExecutionContext) -> dict:

        results = context.results

        if not results:
            return {
                "success": True,
                "confidence": 0.0,
                "summary": "No agents were executed.",
                "recommendations": [],
                "severity": "Unknown",
            }

        # Overall success
        success = all(result.success for result in results)

        # Average confidence
        confidence = round(
            sum(result.confidence for result in results)
            / len(results),
            2,
        )

        # Remove duplicate recommendations
        recommendations = list(
            OrderedDict.fromkeys(
                rec
                for result in results
                for rec in result.recommendations
            )
        )

        # Collect findings
        findings = [
            f"[{result.agent_name}] {result.finding}"
            for result in results
            if result.finding
        ]

        # Collect summaries
        summaries = [
            f"[{result.agent_name}] {result.summary}"
            for result in results
            if result.summary
        ]

        # Determine overall severity
        severity = "Low"

        if confidence >= 0.90:
            severity = "Critical"
        elif confidence >= 0.75:
            severity = "High"
        elif confidence >= 0.50:
            severity = "Medium"

        context.incident_level = severity

        # Human approval
        approval_required = any(
            result.requires_human_approval
            for result in results
        )

        context.requires_human_approval = approval_required

        # Store metadata
        context.metadata["confidence"] = confidence
        context.metadata["severity"] = severity
        context.metadata["approval_required"] = approval_required

        # Executive summary
        summary_parts = []

        if findings:
            summary_parts.append("Key Findings")
            summary_parts.extend(findings)

        if summaries:
            summary_parts.append("")
            summary_parts.append("Agent Analysis")
            summary_parts.extend(summaries)

        summary = "\n".join(summary_parts)

        return {
            "success": success,
            "confidence": confidence,
            "summary": summary,
            "recommendations": recommendations,
            "severity": severity,
        }
```

## mao/workflows/temperature_workflow.py

**File path:** `mao/workflows/temperature_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class TemperatureWorkflow(Workflow):

    name = "temperature_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Evaluate overheating risks.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Temperature Diagnosis",
                description="Determine the cause of abnormal temperature.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve overheating operating procedures.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for overheating equipment.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Recovery Plan",
                description="Create a safe recovery procedure.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## mao/workflows/workflow_engine.py

**File path:** `mao/workflows/workflow_engine.py`

```python
from mao.workflows.workflow import Workflow


class WorkflowEngine:

    def __init__(self):

        self._workflows: dict[str, Workflow] = {}

    def register(self, workflow: Workflow):

        self._workflows[workflow.name] = workflow

    def get(self, name: str):

        return self._workflows.get(name)

    def exists(self, name):

        return name in self._workflows

    def create_tasks(self, workflow_name, event):

        workflow = self.get(workflow_name)

        if workflow is None:

            raise ValueError(
                f"Workflow '{workflow_name}' not found."
            )

        return workflow.build(event)
```

## mao/workflows/workflow.py

**File path:** `mao/workflows/workflow.py`

```python
from abc import ABC, abstractmethod

from mao.events.event import Event
from mao.models.task import Task


class Workflow(ABC):
    """
    Base class for all workflows.
    """

    name: str = "workflow"

    @abstractmethod
    def build(self, event: Event) -> list[Task]:
        """
        Convert an event into executable tasks.
        """
        raise NotImplementedError
```
