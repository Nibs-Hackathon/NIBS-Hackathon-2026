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