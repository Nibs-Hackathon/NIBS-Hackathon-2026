# Folder: backend/mao/workflows Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/mao/workflows`

Contains 11 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/mao/workflows/flow_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/flow_workflow.py`

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

## backend/mao/workflows/gas_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/gas_workflow.py`

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

## backend/mao/workflows/intelligence_tasks.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/intelligence_tasks.py`

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

## backend/mao/workflows/maintenance_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/maintenance_workflow.py`

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

## backend/mao/workflows/planner.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/planner.py`

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

## backend/mao/workflows/policy_engine.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/policy_engine.py`

```python

```

## backend/mao/workflows/pressure_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/pressure_workflow.py`

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

## backend/mao/workflows/supervisor.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/supervisor.py`

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

## backend/mao/workflows/temperature_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/temperature_workflow.py`

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

## backend/mao/workflows/workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/workflow.py`

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

## backend/mao/workflows/workflow_engine.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/workflow_engine.py`

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
