"""Read-only maintenance planning data from the shared MAO runtime."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _result_index() -> dict[tuple[str, str], Any]:
    """Index completed agent output by its workflow task and assigned agent."""
    kernel = runtime.kernel
    return {
        (result.metadata.get("task_name", ""), result.agent_name): result
        for result in kernel.state.agent_results
    }


def _task_asset_name(task: Any, result: Any | None) -> str:
    """Resolve an asset label only when it is present in live task/result data."""
    kernel = runtime.kernel
    input_data = getattr(task, "input_data", {}) or {}
    output_data = getattr(task, "output_data", {}) or {}
    for source in (input_data, output_data, getattr(result, "metadata", {}) or {}):
        asset_id = source.get("asset_name") or source.get("asset_id")
        if asset_id:
            asset = kernel.asset_service.get(asset_id)
            return asset.name if asset else str(asset_id)
    return "Not specified"


def _priority_label(priority: int) -> str:
    return f"P{max(1, min(int(priority), 3))}"


def _work_order_priority(task: Any, result: Any | None) -> str:
    """Prefer the maintenance agent's assessed operational priority."""
    agent_priority = ((getattr(result, "metadata", {}) or {}).get("priority") or "").upper()
    mapping = {"CRITICAL": "P1", "HIGH": "P1", "MEDIUM": "P2", "LOW": "P3"}
    return mapping.get(agent_priority, _priority_label(task.priority))


def _service_provider(asset_type: str) -> str:
    providers = {
        "Pump": "Apex Rotating Services",
        "Compressor": "Apex Rotating Services",
        "Turbine": "Apex Rotating Services",
        "Motor": "VoltWorks Industrial",
        "Generator": "VoltWorks Industrial",
        "Valve": "Precision Instrumentation",
        "Pipeline": "Meridian Pipeline Integrity",
        "Tank": "VesselSafe Engineering",
        "Heat Exchanger": "ThermaCore Services",
        "Reactor": "ProcessWorks Engineering",
    }
    return providers.get(asset_type, "RigOS Certified Maintenance")


def _scheduled_date(priority: str) -> str:
    offsets = {"P1": 1, "P2": 3, "P3": 7}
    return (datetime.now() + timedelta(days=offsets.get(priority, 7))).date().isoformat()


def get_maintenance_plan() -> dict:
    """Format state-manager tasks and agent output for the planner UI."""
    kernel = runtime.kernel
    results = _result_index()
    rows = []
    seen_work = set()
    for task in kernel.state.get_tasks():
        # Sensor, safety, and knowledge tasks are evidence collection—not work
        # orders. The maintenance board should show only planned field work.
        if task.assigned_agent != "maintenance":
            continue
        result = results.get((task.name, task.assigned_agent))
        asset_name = _task_asset_name(task, result)
        asset = next(
            (item for item in kernel.asset_service.all_assets() if item.name == asset_name),
            None,
        )
        priority = _work_order_priority(task, result)
        work_orders = (getattr(result, "metadata", {}) or {}).get("work_orders") if result else None
        for work_order in work_orders or [task.description]:
            key = (asset_name, work_order)
            if key in seen_work:
                continue
            seen_work.add(key)
            rows.append(
                {
                    "Priority": priority,
                    "Asset": asset_name,
                    "Refinery": getattr(asset, "location", "Unassigned"),
                    "Work order": work_order,
                    "Owner": "RigOS Maintenance Planner",
                    "Service provider": _service_provider(getattr(getattr(asset, "asset_type", None), "value", "")),
                    "Scheduled date": _scheduled_date(priority),
                    "Estimated downtime": (getattr(result, "metadata", {}) or {}).get("downtime") or {"P1": "6 hours", "P2": "3 hours", "P3": "1 hour"}.get(priority, "To be assessed"),
                    "State": "Scheduled" if result and result.success else "Planning failed",
                    "Confidence": f"{round(result.confidence * 100)}%" if result else "Not available",
                }
            )

    maintenance_results = [
        result for result in kernel.state.agent_results if result.agent_name == "maintenance"
    ]
    planning_results = [
        result for result in kernel.state.agent_results if result.agent_name == "planning"
    ]
    latest_maintenance = maintenance_results[-1] if maintenance_results else None
    latest_plan = planning_results[-1] if planning_results else None
    owners = defaultdict(int)
    for row in rows:
        owners[row["Owner"]] += 1

    rationale = []
    if latest_plan:
        rationale = latest_plan.recommendations or latest_plan.evidence
    elif latest_maintenance:
        rationale = latest_maintenance.recommendations or latest_maintenance.evidence

    return {
        "tasks": rows,
        "metrics": [
            ("Planned work", str(len(rows)), "From MAO task state", "cyan"),
            ("High priority", str(sum(row["Priority"] == "P1" for row in rows)), "P1 workflow tasks", "red"),
            ("Assigned teams", str(len(owners)), "Derived from task owners", "green"),
            ("Maintenance results", str(len(maintenance_results)), "Live MAO outputs", "violet"),
        ],
        "rationale": rationale,
        "priority": (
            latest_maintenance.metadata.get("priority", "Not available")
            if latest_maintenance
            else "Not available"
        ),
        "downtime": (
            latest_maintenance.metadata.get("downtime", "Not available")
            if latest_maintenance
            else "Not available"
        ),
    }
