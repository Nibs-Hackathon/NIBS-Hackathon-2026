"""Agent adapter using BackendAPI."""

from __future__ import annotations

from app.frontend_services.backend_api_new import api


def get_agents() -> list[dict[str, str]]:
    """Return registered agents and their latest execution state."""
    agents_data = api.get_agents()
    activity = api.get_agent_activity(limit=20)
    
    # Map agent names to latest results
    latest_results = {}
    for a in activity:
        if a["agent_name"] not in latest_results:
            latest_results[a["agent_name"]] = a
    
    agents = []
    for agent in agents_data:
        name = agent["name"]
        result = latest_results.get(name)
        agents.append({
            "Agent": name.replace("_", " ").title(),
            "Specialty": name.title(),
            "State": "Active" if result and result.get("success") else "Ready",
            "Confidence": f"{round(result.get('confidence', 0) * 100)}%" if result else "N/A",
            "Current task": result.get("finding", "Awaiting task")[:50] if result else "Awaiting task",
        })
    return agents


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return monitor metrics calculated from the live state."""
    agents_data = api.get_agents()
    activity = api.get_agent_activity(limit=50)
    status = api.get_simulation_status()
    
    registered = len(agents_data)
    results = len(activity)
    success_count = sum(1 for a in activity if a.get("success"))
    avg_confidence = sum(a.get("confidence", 0) for a in activity) / len(activity) if activity else 0
    
    return [
        ("Agents registered", str(registered), "Shared MAO registry", "green"),
        ("Tasks active", str(status.get("reports", 0)), "Execution reports", "amber"),
        ("Avg. confidence", f"{round(avg_confidence * 100, 1)}%" if avg_confidence else "N/A", "From completed agent results", "cyan"),
        ("Decisions recorded", str(results), "MAO agent executions", "violet"),
    ]