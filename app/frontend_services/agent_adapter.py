"""Read-only agent-monitor view models sourced from the shared MAO runtime."""

from __future__ import annotations

from datetime import datetime, timezone

from services.runtime import kernel


def _latest_result(agent_name: str):
    """Return the newest in-memory result for a registered agent."""
    return next(
        (
            result
            for result in reversed(kernel.state.agent_results)
            if result.agent_name == agent_name
        ),
        None,
    )


def _runtime_seconds(result) -> str:
    """Present the elapsed time since the latest result without inventing duration."""
    if result is None or not getattr(result, "timestamp", None):
        return "Not available"

    timestamp = result.timestamp
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    elapsed = max(0, int((datetime.now(timezone.utc) - timestamp).total_seconds()))
    return f"{elapsed}s ago"


def get_agents() -> list[dict]:
    """Return registered MAO agents with their latest observed execution state."""
    agents = []
    for agent in kernel.registry.all():
        result = _latest_result(agent.name)
        agents.append(
            {
                "Agent": agent.name.replace("_", " ").title(),
                "Specialty": agent.__class__.__name__.replace("Agent", "") or "Operations",
                "State": "Completed" if result and result.success else ("Attention" if result else "Ready"),
                "Last execution": _runtime_seconds(result),
                "Runtime": _runtime_seconds(result),
                "Confidence": f"{round(result.confidence * 100)}%" if result else "Not available",
                "Decision": (
                    result.decision or result.summary or result.finding or "Awaiting an assigned workflow task"
                )
                if result
                else "Awaiting an assigned workflow task",
                "Success": "Yes" if result and result.success else ("No" if result else "Not available"),
                "Current task": (
                    result.metadata.get("task_name", "Latest completed task") if result else "Awaiting task"
                ),
            }
        )
    return agents


def get_agent_monitor_metrics(agents: list[dict] | None = None) -> list[tuple[str, str, str, str]]:
    """Summarize registered agents from runtime state without synthetic values."""
    agents = agents if agents is not None else get_agents()
    result_count = len(kernel.state.agent_results)
    completed = sum(1 for agent in agents if agent["State"] == "Completed")
    attention = sum(1 for agent in agents if agent["State"] == "Attention")
    confidences = [
        result.confidence for result in kernel.state.agent_results if result.confidence is not None
    ]
    average = f"{round((sum(confidences) / len(confidences)) * 100, 1)}%" if confidences else "Not available"

    return [
        ("Registered agents", str(len(agents)), "From shared MAO registry", "cyan"),
        ("Completed agents", str(completed), "Latest execution state", "green"),
        ("Agent attention", str(attention), "Latest failed result", "amber" if attention else "green"),
        ("Agent decisions", str(result_count), f"Average confidence {average}", "violet"),
    ]
