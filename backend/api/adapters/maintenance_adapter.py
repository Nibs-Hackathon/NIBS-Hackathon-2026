"""Read-only maintenance planning data from the shared MAO runtime."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import sys
from threading import Lock
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime
from services.local_mode import local_demo_mode


_DEMO_WORK_ORDERS: list[dict[str, Any]] = []
_DEMO_WORK_ORDERS_LOCK = Lock()


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

    persisted = _persisted_work_orders()
    for row in persisted:
        key = (row.get("Asset"), row.get("Work order"))
        if key in seen_work:
            continue
        seen_work.add(key)
        rows.append(row)
        owners[row.get("Owner") or "Operator"] += 1

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


def _persisted_work_orders() -> list[dict[str, Any]]:
    """Load operator-created work orders from ActionDB."""
    if local_demo_mode():
        with _DEMO_WORK_ORDERS_LOCK:
            return [dict(row) for row in _DEMO_WORK_ORDERS]

    try:
        from database.connection import get_session
        from database.models import ActionDB

        session = get_session()
        try:
            actions = (
                session.query(ActionDB)
                .filter(ActionDB.action_type.in_(["work_order", "work_order_create"]))
                .order_by(ActionDB.created_at.desc())
                .limit(100)
                .all()
            )
            rows = []
            for action in actions:
                payload = action.payload or {}
                asset = runtime.kernel.asset_service.get(action.asset_id) if action.asset_id else None
                status = "Scheduled" if action.status == "approved" else (
                    "Ready" if action.status == "pending_approval" else action.status or "Backlog"
                )
                rows.append({
                    "id": action.id,
                    "Priority": payload.get("priority") or "P2",
                    "Asset": payload.get("asset_name") or getattr(asset, "name", action.asset_id),
                    "asset_id": action.asset_id,
                    "Refinery": payload.get("refinery") or getattr(asset, "location", "Unassigned"),
                    "Work order": payload.get("title") or payload.get("description") or "Operator work order",
                    "title": payload.get("title") or payload.get("description") or "Operator work order",
                    "Owner": payload.get("owner") or action.requested_by or "Control operator",
                    "Service provider": payload.get("service_provider") or "RigOS Certified Maintenance",
                    "Scheduled date": payload.get("scheduled_date"),
                    "Estimated downtime": payload.get("downtime") or "To be assessed",
                    "estimated_cost": payload.get("estimated_cost"),
                    "cost": payload.get("estimated_cost"),
                    "State": status,
                    "status": status,
                    "Confidence": "Operator requested",
                    "source": "operator_action",
                })
            return rows
        finally:
            session.close()
    except Exception:
        return []


def create_work_order(
    *,
    asset_id: str | None = None,
    title: str,
    priority: str = "P2",
    owner: str = "Control operator",
    downtime: str | None = None,
    estimated_cost: float | None = None,
    note: str | None = None,
    incident_id: str | None = None,
) -> dict[str, Any]:
    """Persist a new work-order request as an ActionDB audit row."""
    from uuid import uuid4

    asset = runtime.kernel.asset_service.get(asset_id) if asset_id else None
    action_id = str(uuid4())

    if local_demo_mode():
        row = {
            "id": action_id,
            "Priority": priority,
            "Asset": getattr(asset, "name", asset_id) or "Not specified",
            "asset_id": asset_id,
            "Refinery": getattr(asset, "location", "Unassigned"),
            "Work order": title,
            "title": title,
            "Owner": owner,
            "Service provider": _service_provider(
                getattr(getattr(asset, "asset_type", None), "value", "")
            ),
            "Scheduled date": None,
            "Estimated downtime": downtime or "To be assessed",
            "estimated_cost": estimated_cost,
            "cost": estimated_cost,
            "State": "Ready",
            "status": "pending_approval",
            "Confidence": "Operator requested",
            "source": "local_demo",
            "incident_id": incident_id,
            "note": note,
        }
        with _DEMO_WORK_ORDERS_LOCK:
            _DEMO_WORK_ORDERS.insert(0, row)
        return {
            "id": action_id,
            "asset_id": asset_id,
            "title": title,
            "priority": priority,
            "status": "pending_approval",
            "owner": owner,
            "downtime": downtime,
            "estimated_cost": estimated_cost,
            "message": "Work order recorded in the local demo session for approval.",
        }

    from database.connection import get_session
    from database.models import ActionDB

    session = get_session()
    try:
        action = ActionDB(
            id=action_id,
            incident_id=incident_id,
            asset_id=asset_id,
            action_type="work_order",
            payload={
                "title": title,
                "description": title,
                "priority": priority,
                "owner": owner,
                "downtime": downtime,
                "estimated_cost": estimated_cost,
                "asset_name": getattr(asset, "name", None),
                "refinery": getattr(asset, "location", None),
                "note": note,
            },
            risk_level="HIGH" if str(priority).upper() in {"P1", "CRITICAL", "HIGH"} else "MEDIUM",
            status="pending_approval",
            requires_human_approval=True,
            requested_by=owner,
        )
        session.add(action)
        session.commit()
        return {
            "id": action.id,
            "asset_id": asset_id,
            "title": title,
            "priority": priority,
            "status": action.status,
            "owner": owner,
            "downtime": downtime,
            "estimated_cost": estimated_cost,
            "message": "Work order recorded for approval. No industrial command was executed.",
        }
    finally:
        session.close()


def approve_work_order(work_order_id: str, *, operator: str = "Maintenance lead", note: str | None = None) -> dict[str, Any]:
    """Approve a pending work-order ActionDB row."""
    if local_demo_mode():
        with _DEMO_WORK_ORDERS_LOCK:
            action = next(
                (row for row in _DEMO_WORK_ORDERS if row.get("id") == work_order_id),
                None,
            )
            if action is None:
                raise LookupError(f"Work order {work_order_id} not found")
            action["State"] = "Scheduled"
            action["status"] = "approved"
            action["approved_by"] = operator
            if note:
                action["approval_note"] = note
        return {
            "id": work_order_id,
            "status": "approved",
            "approved_by": operator,
            "message": "Work order approved in the local demo session.",
        }

    from datetime import datetime
    from database.connection import get_session
    from database.models import ActionDB

    session = get_session()
    try:
        action = session.query(ActionDB).filter(ActionDB.id == work_order_id).first()
        if action is None:
            raise LookupError(f"Work order {work_order_id} not found")
        if action.action_type not in {"work_order", "work_order_create"}:
            raise ValueError("Action is not a work order")
        payload = dict(action.payload or {})
        if note:
            payload["approval_note"] = note
        action.payload = payload
        action.status = "approved"
        action.approved_by = operator
        action.executed_at = datetime.utcnow()
        action.requires_human_approval = False
        session.add(action)
        session.commit()
        return {
            "id": action.id,
            "status": action.status,
            "approved_by": operator,
            "message": "Work order approved. No industrial command was executed.",
        }
    finally:
        session.close()

