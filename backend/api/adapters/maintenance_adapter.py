"""Read-only maintenance planning data from the shared MAO runtime."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _notify_work_order(action_id: str, title: str, status: str, asset_id: str | None = None) -> None:
    """Publish work-order state changes into the operator inbox."""
    try:
        from uuid import uuid4
        from services.notification_service import (
            Notification,
            NotificationSeverity,
            NotificationType,
            notification_service,
        )

        severity = (
            NotificationSeverity.WARNING
            if status == "pending_approval"
            else NotificationSeverity.SUCCESS
            if status in {"approved", "completed"}
            else NotificationSeverity.INFO
        )
        notification_service.add_notification(Notification(
            id=str(uuid4()),
            type=NotificationType.MAINTENANCE_SCHEDULED,
            severity=severity,
            title=f"Work order {status.replace('_', ' ')}",
            message=title,
            asset_id=asset_id,
            metadata={"work_order_id": action_id, "status": status},
            human_approval_required=status == "pending_approval",
        ))
    except Exception:
        return


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
    work_index = {}
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
            task_id = getattr(task, "id", None) or getattr(task, "task_id", None)
            if task_id:
                stable_id = f"plan-{task_id}"
            else:
                stable_id = "plan-" + hashlib.md5(f"{asset_name}:{work_order}".encode()).hexdigest()[:12]
            meta = getattr(result, "metadata", {}) or {}
            rows.append(
                {
                    "id": stable_id,
                    "Priority": priority,
                    "Asset": asset_name,
                    "asset_id": getattr(asset, "id", None),
                    "incident_id": meta.get("incident_id"),
                    "Refinery": getattr(asset, "location", "Unassigned"),
                    "Work order": work_order,
                    "title": work_order,
                    "Owner": "RigOS Maintenance Planner",
                    "Service provider": _service_provider(getattr(getattr(asset, "asset_type", None), "value", "")),
                    "Scheduled date": _scheduled_date(priority),
                    "Estimated downtime": meta.get("downtime") or "To be assessed",
                    # A successful MAO plan is ready for operator approval; it
                    # is not scheduled field work until that approval persists.
                    "State": "Ready" if result and result.success else "Backlog",
                    "status": "Ready" if result and result.success else "Backlog",
                    "Confidence": f"{round(result.confidence * 100)}%" if result else "Not available",
                    "source": "mao_plan",
                }
            )
            work_index[key] = len(rows) - 1

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
            # The persisted operator record is authoritative over its original
            # AI proposal, especially after approval changes the status.
            rows[work_index[key]] = {**rows[work_index[key]], **row}
            continue
        seen_work.add(key)
        rows.append(row)
        work_index[key] = len(rows) - 1
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
    from database.connection import get_session
    from database.models import ActionDB

    asset = runtime.kernel.asset_service.get(asset_id) if asset_id else None
    session = get_session()
    try:
        action = ActionDB(
            id=str(uuid4()),
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
        _notify_work_order(action.id, title, action.status, asset_id)
        return {
            "id": action.id,
            "incident_id": incident_id,
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
        _notify_work_order(
            action.id,
            payload.get("title") or "Maintenance work order",
            action.status,
            action.asset_id,
        )
        return {
            "id": action.id,
            "status": action.status,
            "approved_by": operator,
            "message": "Work order approved. No industrial command was executed.",
        }
    finally:
        session.close()


def transition_work_order(
    work_order_id: str,
    *,
    status: str,
    operator: str = "Maintenance lead",
    note: str | None = None,
) -> dict[str, Any]:
    """Advance an approved work order through its auditable field-work lifecycle."""
    from datetime import datetime
    from database.connection import get_session
    from database.models import ActionDB

    requested = str(status or "").strip().lower().replace(" ", "_")
    allowed = {"approved": {"in_progress"}, "in_progress": {"completed"}}
    session = get_session()
    try:
        action = session.query(ActionDB).filter(ActionDB.id == work_order_id).first()
        if action is None:
            raise LookupError(f"Work order {work_order_id} not found")
        if action.action_type not in {"work_order", "work_order_create"}:
            raise ValueError("Action is not a work order")
        current = str(action.status or "").lower().replace(" ", "_")
        if requested not in allowed.get(current, set()):
            raise ValueError(f"Work order cannot move from {current or 'unknown'} to {requested}")
        payload = dict(action.payload or {})
        history = list(payload.get("status_history") or [])
        history.append({
            "from": current,
            "to": requested,
            "operator": operator,
            "note": note,
            "at": datetime.utcnow().isoformat(),
        })
        payload["status_history"] = history
        action.payload = payload
        action.status = requested
        action.approved_by = action.approved_by or operator
        action.executed_at = datetime.utcnow()
        session.add(action)
        session.commit()
        incident_resolution = {
            "resolved": False,
            "incident_id": action.incident_id,
            "reason": "Work remains open or no matching active simulator incident exists",
        }
        if requested == "completed" and action.asset_id:
            simulator = getattr(runtime, "active_simulator", None)
            if simulator is not None:
                incident_resolution = simulator.complete_field_work(
                    action.asset_id,
                    incident_id=action.incident_id,
                )
        _notify_work_order(
            action.id,
            payload.get("title") or "Maintenance work order",
            requested,
            action.asset_id,
        )
        return {
            "id": action.id,
            "status": requested,
            "operator": operator,
            "incident_resolution": incident_resolution,
            "message": (
                "Work order completed, linked simulator incident resolved, and audit trail updated."
                if requested == "completed" and incident_resolution.get("resolved")
                else "Work order completed and recorded in the audit trail."
                if requested == "completed"
                else "Work order marked in progress. No industrial command was executed."
            ),
        }
    finally:
        session.close()

