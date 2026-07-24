# Folder: tests Code Inventory

Generated: 2026-07-24T03:28:50 UTC

Contains 8 project files.

## tests/conftest.py

**File path:** `tests/conftest.py`

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from mao.core.context import ExecutionContext


class DummyEvent:
    def __init__(self, payload):
        self.payload = payload


@pytest.fixture
def normal_context():
    event = DummyEvent(
        {
            "pressure": 120,
            "temperature": 50,
            "gas_level": 5,
            "vibration": 2,
            "flow_rate": 80,
        }
    )

    return ExecutionContext(
        event,
        state_manager=None,
        memory_manager=None,
        logger=None,
    )


@pytest.fixture
def critical_context():

    event = DummyEvent(
        {
            "pressure": 170,
            "temperature": 95,
            "gas_level": 60,
            "vibration": 10,
            "flow_rate": 20,
        }
    )

    return ExecutionContext(
        event,
        state_manager=None,
        memory_manager=None,
        logger=None,
    )
```

## tests/test_agent_pipeline.py

**File path:** `tests/test_agent_pipeline.py`

```python
from unittest.mock import MagicMock

from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent
from agents.planning import PlanningAgent
from agents.knowledge import KnowledgeAgent

from mao.models.task import Task


def test_pipeline(critical_context):

    SafetyAgent().run(
        Task(
            name="Safety",
            description="Safety Assessment",
            assigned_agent="safety",
            priority=1,
        ),
        critical_context
    )

    DiagnosticAgent().run(
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
        ),
        critical_context
    )

    MaintenanceAgent().run(
        Task(
            name="Maintenance",
            description="Generate maintenance plan",
            assigned_agent="maintenance",
            priority=3,
        ),
        critical_context
    )

    PlanningAgent().run(
        Task(
            name="Planning",
            description="Generate execution plan",
            assigned_agent="planning",
            priority=4,
        ),
        critical_context
    )

    agent = KnowledgeAgent(
        MagicMock()
    )

    agent.retriever = MagicMock()

    agent.retriever.retrieve.return_value = []

    agent.run(
        Task(
            name="Knowledge",
            description="Retrieve knowledge",
            assigned_agent="knowledge",
            priority=5,
        ),
        critical_context
    )

    expected = [
        "safety",
        "diagnosis",
        "maintenance",
        "planning",
        "knowledge",
    ]

    for key in expected:
        assert key in critical_context.metadata
```

## tests/test_diagnostic_agent.py

**File path:** `tests/test_diagnostic_agent.py`

```python
from agents.diagnostic import DiagnosticAgent
from agents.safety import SafetyAgent
from mao.models.task import Task


safety_task = Task(
    name="Safety",
    description="Safety Assessment",
    assigned_agent="safety",
    priority=1,
)

diag_task = Task(
    name="Diagnosis",
    description="Run diagnostics",
    assigned_agent="diagnostic",
    priority=2,
)

def test_diagnosis(critical_context):

    SafetyAgent().run(
        safety_task,
        critical_context,
    )

    result = DiagnosticAgent().run(
        diag_task,
        critical_context,
    )

    assert result.success

    assert "diagnosis" in critical_context.metadata

    diagnosis = critical_context.metadata["diagnosis"]

    assert len(diagnosis["diagnosis"]) > 0
```

## tests/test_knowledge_agent.py

**File path:** `tests/test_knowledge_agent.py`

```python
from unittest.mock import MagicMock

from agents.knowledge import KnowledgeAgent

from mao.models.task import Task


def test_knowledge():

    retriever = MagicMock()

    retriever.retrieve.return_value = []

    vector_store = MagicMock()

    agent = KnowledgeAgent(vector_store)

    agent.retriever = retriever

    from mao.core.context import ExecutionContext


    class Event:
        payload = {}


    context = ExecutionContext(
        Event(),
        None,
        None,
        None,
    )

    result = agent.run(
        Task(
            name="Knowledge",
            description="Retrieve knowledge",
            assigned_agent="knowledge",
            priority=5,
        ),
        context,
    )

    assert result.success

    assert "knowledge" in context.metadata
```

## tests/test_maintenance_agent.py

**File path:** `tests/test_maintenance_agent.py`

```python
from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent

from mao.models.task import Task


def test_maintenance_plan(critical_context):

    SafetyAgent().run(Task(
            name="Safety",
            description="Safety Assessment",
            assigned_agent="safety",
            priority=1,
        ),
        critical_context,
    )
    

    DiagnosticAgent().run(
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
            
        ),
        critical_context,
    )

    result = MaintenanceAgent().run(
        Task(
            name="Maintenance",
            description="Generate maintenance plan",
            assigned_agent="maintenance",
            priority=3,
        ),
        critical_context,
    )

    assert result.success

    metadata = critical_context.metadata["maintenance"]

    assert "priority" in metadata

    assert "work_orders" in metadata

    assert len(metadata["work_orders"]) > 0
```

## tests/test_neon.py

**File path:** `tests/test_neon.py`

```python
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
conn = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

print("connected to database")
conn.close()
```

## tests/test_planning_agent.py

**File path:** `tests/test_planning_agent.py`

```python
from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent
from agents.planning import PlanningAgent

from mao.models.task import Task


def test_plan_generation(critical_context):

    SafetyAgent().run(
        Task(
            name="Safety",
            description="Safety Assessment",
            assigned_agent="safety",
            priority=1,
        ),
        critical_context
    )

    DiagnosticAgent().run(
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
        ),
        critical_context
    )

    MaintenanceAgent().run(
  
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
        ),
        critical_context
    )

    result = PlanningAgent().run(
        Task(
            name="Planning",
            description="Generate execution plan",
            assigned_agent="planning",
            priority=4,
        ),
        critical_context,   
    )

    assert result.success

    assert "planning" in critical_context.metadata

    plan = critical_context.metadata["planning"]

    assert len(plan["execution_plan"]) > 0
```

## tests/test_safety_agent.py

**File path:** `tests/test_safety_agent.py`

```python
from agents.safety import SafetyAgent
from mao.models.task import Task


task = Task(
    name="Safety",
    description="",
    assigned_agent="safety",
    priority=1,
)


def test_safe_system(normal_context):

    agent = SafetyAgent()

    result = agent.run(task, normal_context)

    assert result.success
    assert result.confidence > 0

    assert "safety" in normal_context.metadata

    assert (
        normal_context.metadata["safety"]["status"]
        == "SAFE"
    )


def test_critical_system(critical_context):

    agent = SafetyAgent()

    result = agent.run(task, critical_context)

    assert result.success

    metadata = critical_context.metadata["safety"]

    assert metadata["status"] == "CRITICAL"

    assert metadata["risk_score"] >= 80

    assert len(metadata["alerts"]) > 0
```
