# Folder: backend/mao/models Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/mao/models`

Contains 4 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/mao/models/execution_report.py

**Folder path:** `backend/mao/models`

**File path:** `backend/mao/models/execution_report.py`

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

## backend/mao/models/notification.py

**Folder path:** `backend/mao/models`

**File path:** `backend/mao/models/notification.py`

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

## backend/mao/models/result.py

**Folder path:** `backend/mao/models`

**File path:** `backend/mao/models/result.py`

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

## backend/mao/models/task.py

**Folder path:** `backend/mao/models`

**File path:** `backend/mao/models/task.py`

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
