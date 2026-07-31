# Folder: backend/mao/core Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/mao/core`

Contains 7 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/mao/core/context.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/context.py`

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

## backend/mao/core/exceptions.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/exceptions.py`

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

## backend/mao/core/executor.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/executor.py`

```python
"""Optimized executor with parallel processing and timeout."""

import concurrent.futures
import time
from typing import Optional
from mao.models.result import AgentResult
from mao.core.exceptions import AgentNotFound


class Executor:
    def __init__(self, registry, max_workers: int = 4, timeout: int = 30):
        self.registry = registry
        self.max_workers = max_workers
        self.timeout = timeout
        self.execution_stats = {}

    def execute(self, task, context):
        agent = self.registry.get(task.assigned_agent)

        if agent is None:
            raise AgentNotFound(f"Agent '{task.assigned_agent}' not found.")

        start = time.time()
        
        try:
            # Execute with timeout
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(agent.run, task, context)
                try:
                    result = future.result(timeout=self.timeout)
                except concurrent.futures.TimeoutError:
                    raise TimeoutError(f"Agent {agent.name} exceeded {self.timeout}s timeout")

            elapsed = time.time() - start
            
            # Track stats
            self.execution_stats[agent.name] = {
                "last_execution": elapsed,
                "total_executions": self.execution_stats.get(agent.name, {}).get("total_executions", 0) + 1,
                "avg_time": 0
            }
            
            stats = self.execution_stats[agent.name]
            total = stats["total_executions"]
            avg = (stats.get("avg_time", 0) * (total - 1) + elapsed) / total
            stats["avg_time"] = round(avg, 2)

        except Exception as e:
            elapsed = time.time() - start
            result = AgentResult(
                agent_name=agent.name,
                success=False,
                finding="Agent execution failed.",
                confidence=0.0,
                summary=str(e),
                recommendations=["Review execution logs."],
                metadata={"exception": type(e).__name__, "execution_time": elapsed},
            )

        result.metadata.update({
            "task_name": task.name,
            "task_description": task.description,
            "event_name": context.event.name,
            "asset_id": context.event.source,
            "execution_time": elapsed,
        })

        return result

    def get_stats(self):
        """Get execution statistics for all agents."""
        return self.execution_stats
```

## backend/mao/core/logger.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/logger.py`

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

## backend/mao/core/registry.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/registry.py`

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

## backend/mao/core/scheduler.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/scheduler.py`

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

## backend/mao/core/state_manager.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/state_manager.py`

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
