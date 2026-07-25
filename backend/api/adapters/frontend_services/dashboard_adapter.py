"""Dashboard adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def calculate_severity(event):
    """Calculate severity from event payload."""
    payload = event.get("payload", {})

    if "gas" in payload:
        return "Critical"
    if "pressure" in payload:
        return "Critical" if payload["pressure"] > 160 else "High"
    if "temperature" in payload:
        return "Critical" if payload["temperature"] > 100 else "High"
    if "vibration" in payload:
        return "Critical" if payload["vibration"] > 40 else "High"
    if "flow" in payload:
        return "Medium"
    return "Unknown"


def get_dashboard():
    """Get dashboard data using BackendAPI with caching."""
    # Get data from API (uses caching internally)
    assets = api.get_assets()
    incidents = api.get_incidents()
    activity = api.get_agent_activity(limit=5)

    # ✅ Use runtime.kernel
    kernel = runtime.kernel

    # Calculate metrics
    total_assets = len(assets)
    healthy_assets = sum(1 for a in assets if a.get("status") == "Running")
    avg_health = sum(a.get("health", 0) for a in assets) / total_assets if total_assets else 0

    metrics = [
        ("Fleet health", f"{avg_health:.1f}%", "Calculated from assets", "green"),
        ("Assets online", f"{healthy_assets} / {total_assets}", "Connected", "cyan"),
        ("Active incidents", str(len(incidents)), "From EventStore", "red"),
        ("AI decisions", str(len(kernel.state.agent_results)), "Agent executions", "violet"),
    ]

    # Format incidents
    formatted_incidents = []
    for incident in incidents[-10:]:
        formatted_incidents.append({
            "Incident": incident.get("name", "Unknown"),
            "Asset": incident.get("asset_id", "Unknown"),
            "Severity": calculate_severity(incident),
            "Detected": incident.get("timestamp", "").split("T")[1][:8] if "T" in incident.get("timestamp", "") else "",
        })

    # Format activity
    formatted_activity = []
    for a in activity[:5]:
        timestamp = a.get("timestamp", "")
        time_str = timestamp.split("T")[1][:8] if "T" in timestamp else ""
        formatted_activity.append((
            time_str,
            a.get("agent_name", "Unknown"),
            a.get("summary", "")[:100],
        ))

    return {
        "metrics": metrics,
        "incidents": formatted_incidents,
        "assets": assets,
        "activity": formatted_activity,
    }