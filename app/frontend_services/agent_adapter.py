"""Read-only view model for the agents registered on the shared MAO kernel."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel



def get_agents() -> list[dict[str, str]]:
    """Return registered agents and their latest execution state.

    ``AgentRegistry`` intentionally exposes ``all()`` rather than its private
    ``_agents`` dictionary.  Keeping that boundary here prevents the UI from
    breaking when the registry implementation changes.
    """
    agents = []
    for agent in kernel.registry.all():
        name = getattr(agent, "name", agent.__class__.__name__)
        result = get_latest_result(name)
        metadata = getattr(result, "metadata", {}) if result else {}
        agents.append(
            {
                "Agent": name.replace("_", " ").title(),
                "Specialty": agent.__class__.__name__.removesuffix("Agent"),
                "State": "Active" if result else "Ready",
                "Confidence": f"{round(result.confidence * 100)}%" if result else "N/A",
                "Current task": metadata.get("task_name", "Awaiting task"),
            }
        )
    return agents




def get_latest_result(agent_name: str):
    """Return the newest result for an agent, if the agent has run."""
    results = [
        result for result in kernel.state.agent_results
        if getattr(result, "agent_name", None) == agent_name
    ]
    return results[-1] if results else None


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return monitor metrics calculated from the live MAO state."""
    registered = kernel.registry.all()
    results = kernel.state.agent_results
    tasks = kernel.state.get_tasks()
    average_confidence = (
        sum(result.confidence for result in results) / len(results)
        if results else None
    )
    active_tasks = sum(
        str(getattr(task, "status", "")).upper().endswith("RUNNING")
        for task in tasks
    )
    return [
        ("Agents registered", str(len(registered)), "Shared MAO registry", "green"),
        ("Tasks active", str(active_tasks), f"{len(tasks)} task(s) tracked", "amber"),
        (
            "Avg. confidence",
            f"{round(average_confidence * 100, 1)}%" if average_confidence is not None else "N/A",
            "From completed agent results" if results else "No executions yet",
            "cyan",
        ),
        ("Decisions recorded", str(len(results)), "MAO agent executions", "violet"),
    ]
