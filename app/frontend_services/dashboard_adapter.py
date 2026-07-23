"""Read-only executive dashboard model built from the singleton MAO runtime."""

from __future__ import annotations

from collections import defaultdict

from services.runtime import kernel


def calculate_severity(event) -> str:
    payload = event.payload or {}
    if "gas" in payload or "gas_level" in payload:
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


def calculate_average_health(assets) -> float | None:
    if not assets:
        return None
    return round(sum(asset.health for asset in assets) / len(assets), 1)


def _asset_snapshot(assets) -> list[dict]:
    return [
        {
            "Asset": asset.name,
            "Type": getattr(asset.asset_type, "value", str(asset.asset_type)),
            "Zone": asset.location or "Unassigned",
            "Health": asset.health,
            "Status": asset.status or "Unknown",
        }
        for asset in assets
    ]


def _zone_health(assets) -> list[dict]:
    zones: dict[str, list[float]] = defaultdict(list)
    for asset in assets:
        zones[asset.location or "Unassigned"].append(asset.health)
    return [
        {"zone": zone, "health": round(sum(values) / len(values), 1)}
        for zone, values in sorted(zones.items())
    ]


def get_dashboard() -> dict:
    """Return dashboard data from live runtime state; this function never simulates data."""
    assets = kernel.asset_service.all_assets()
    incidents = [
        {
            "Incident": event.name,
            "Asset": event.source,
            "Severity": calculate_severity(event),
            "Detected": event.timestamp.strftime("%H:%M:%S"),
        }
        for event in kernel.event_store.all()
    ]
    reports = kernel.state.execution_reports
    tasks = kernel.state.get_tasks()
    notifications = kernel.state.get_notifications()
    predictions = [result for result in kernel.state.agent_results if result.agent_name == "prediction"]
    average_health = calculate_average_health(assets)
    active_assets = sum(1 for asset in assets if str(asset.status).lower() not in {"offline", "inactive"})
    pending_tasks = sum(
        1 for task in tasks if getattr(getattr(task, "status", None), "value", str(getattr(task, "status", ""))).lower() not in {"completed", "cancelled"}
    )

    metrics = [
        ("System health", f"{average_health}%" if average_health is not None else "Not available", "Calculated from registered assets", "green"),
        ("Active assets", f"{active_assets} / {len(assets)}", "Registered runtime assets", "cyan"),
        ("Open incidents", str(len(incidents)), "Current EventStore entries", "red"),
        ("AI workflows", str(len(reports)), "Completed MAO execution reports", "violet"),
        ("Pending maintenance", str(pending_tasks), "StateManager workflow tasks", "amber"),
        ("Active notifications", str(len(notifications)), "Runtime notification state", "cyan"),
        ("Predictions", str(len(predictions)), "Prediction agent results", "violet"),
        ("Recent reports", str(len(reports)), "Runtime decision records", "green"),
    ]
    activity = [
        {
            "time": str(report.completed_at),
            "actor": "MAO workflow",
            "text": report.final_summary or "Workflow completed without a recorded summary.",
            "status": "Completed" if report.success else "Attention",
        }
        for report in reports[-5:]
    ]
    telemetry = [
        {"Asset": asset.name, "Health": asset.health}
        for asset in assets
    ]
    return {
        "metrics": metrics,
        "incidents": incidents,
        "assets": _asset_snapshot(assets),
        "activity": activity,
        "zones": _zone_health(assets),
        "telemetry": telemetry,
        "is_empty": not any((assets, incidents, reports, kernel.state.agent_results)),
    }
