"""Read models for the RigOS Operations Center.

This module deliberately composes the existing MAO runtime and persistence
records.  It does not alter agent, simulator, or database behaviour.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from api.adapters.backend_api_new import api
from services.runtime import runtime


def _iso(value: Any) -> str | None:
    return value.isoformat() if hasattr(value, "isoformat") else None


def _seconds_between(start: Any, end: Any) -> float | None:
    if not start or not end:
        return None
    return round(max(0, (end - start).total_seconds()), 2)


def _severity_from_payload(payload: dict[str, Any]) -> str:
    if "gas" in payload:
        return "Critical"
    if "pressure" in payload:
        return "Critical" if payload["pressure"] > 160 else "High"
    if "temperature" in payload:
        return "Critical" if payload["temperature"] > 100 else "High"
    if "vibration" in payload:
        return "Critical" if payload["vibration"] > 40 else "High"
    return "Medium" if "flow" in payload else "Unknown"


def _agent_step(execution: Any) -> dict[str, Any]:
    metadata = execution.metadata or {}
    duration = metadata.get("execution_time")
    return {
        "id": execution.id,
        "kind": "agent",
        "agent": execution.agent_name,
        "title": metadata.get("task_name") or execution.agent_name.replace("_", " ").title(),
        "status": "completed" if execution.success else "failed",
        "timestamp": _iso(execution.timestamp),
        "reasoning": execution.summary or execution.output or execution.task,
        "evidence": execution.evidence or [],
        "confidence": execution.confidence,
        "duration_seconds": round(float(duration), 2) if duration is not None else None,
        "output": execution.decision or execution.summary or execution.output,
        "recommendations": execution.recommendations or [],
        "requires_human_approval": bool(execution.requires_human_approval),
    }


def _action_step(action: Any) -> dict[str, Any]:
    return {
        "id": action.id,
        "kind": "operator_action",
        "agent": None,
        "title": action.action_type.replace("_", " ").title(),
        "status": action.status,
        "timestamp": _iso(action.executed_at or action.created_at),
        "reasoning": None,
        "evidence": [],
        "confidence": None,
        "duration_seconds": None,
        "output": action.payload or {},
        "recommendations": [],
        "requires_human_approval": bool(action.requires_human_approval),
        "approved_by": action.approved_by,
    }


def _runtime_incidents(limit: int) -> list[dict[str, Any]]:
    """Graceful live fallback when PostgreSQL is not available."""
    incidents = []
    for event in reversed(runtime.kernel.event_store.all()[-limit:]):
        payload = getattr(event, "payload", {}) or {}
        asset = runtime.kernel.asset_service.get(getattr(event, "source", ""))
        incidents.append({
            "id": event.id,
            "timestamp": _iso(event.timestamp),
            "severity": _severity_from_payload(payload),
            "asset_id": event.source,
            "asset_name": getattr(asset, "name", event.source),
            "incident_type": event.name,
            "status": "recorded",
            "health_before": None,
            "health_after": getattr(asset, "health", None),
            "health_capture_status": "not persisted for this runtime event",
            "operator_actions": [],
            "ai_recommendation": None,
            "execution_report": None,
            "resolution_seconds": None,
            "timeline": [{
                "id": event.id,
                "kind": "incident",
                "agent": None,
                "title": "Incident detected",
                "status": "detected",
                "timestamp": _iso(event.timestamp),
                "reasoning": "Simulator emitted an operational event.",
                "evidence": [f"{key}: {value}" for key, value in payload.items()],
                "confidence": None,
                "duration_seconds": None,
                "output": payload,
                "recommendations": [],
                "requires_human_approval": False,
            }],
        })
    return incidents


def get_incident_audit(limit: int = 100) -> list[dict[str, Any]]:
    """Return durable, incident-centred MAO audit records.

    The database is preferred because runtime EventStore data is intentionally
    ephemeral. A live fallback keeps the control room useful during a database
    outage without presenting it as durable audit history.
    """
    session = None
    try:
        from database.connection import get_session
        from database.models import ActionDB, AgentExecutionDB, ExecutionReportDB, IncidentDB

        session = get_session()
        records = (
            session.query(IncidentDB)
            .order_by(IncidentDB.created_at.desc())
            .limit(limit)
            .all()
        )
        audits = []
        for incident in records:
            report = (
                session.query(ExecutionReportDB)
                .filter(ExecutionReportDB.incident_id == incident.id)
                .order_by(ExecutionReportDB.completed_at.desc())
                .first()
            )
            executions = (
                session.query(AgentExecutionDB)
                .filter(AgentExecutionDB.incident_id == incident.id)
                .order_by(AgentExecutionDB.timestamp.asc())
                .all()
            )
            actions = (
                session.query(ActionDB)
                .filter(ActionDB.incident_id == incident.id)
                .order_by(ActionDB.created_at.asc())
                .all()
            )
            asset = runtime.kernel.asset_service.get(incident.asset_id)
            timeline = [{
                "id": incident.id,
                "kind": "incident",
                "agent": None,
                "title": incident.event,
                "status": "detected",
                "timestamp": _iso(incident.created_at),
                "reasoning": "Operational event persisted by the simulator and MAO kernel.",
                "evidence": [],
                "confidence": None,
                "duration_seconds": None,
                "output": None,
                "recommendations": [],
                "requires_human_approval": False,
            }]
            timeline.extend(_agent_step(execution) for execution in executions)
            timeline.extend(_action_step(action) for action in actions)
            if report:
                timeline.append({
                    "id": report.id,
                    "kind": "report",
                    "agent": "report",
                    "title": "Execution report",
                    "status": "resolved" if report.success else "requires_review",
                    "timestamp": _iso(report.completed_at),
                    "reasoning": report.summary,
                    "evidence": [],
                    "confidence": None,
                    "duration_seconds": _seconds_between(report.started_at, report.completed_at),
                    "output": report.summary,
                    "recommendations": report.recommendations or [],
                    "requires_human_approval": False,
                })
            timeline.sort(key=lambda item: item["timestamp"] or "")
            audits.append({
                "id": incident.id,
                "timestamp": _iso(incident.created_at),
                "severity": incident.severity,
                "asset_id": incident.asset_id,
                "asset_name": getattr(asset, "name", incident.asset_id),
                "incident_type": incident.event,
                "status": incident.status,
                # Historic before/after health was not captured by the original
                # schema. Never infer it as an audit fact.
                "health_before": None,
                "health_after": getattr(asset, "health", None),
                "health_capture_status": "before not captured; after is current asset health",
                "operator_actions": [_action_step(action) for action in actions],
                "ai_recommendation": (report.recommendations[0] if report and report.recommendations else None),
                "execution_report": {
                    "id": report.id,
                    "summary": report.summary,
                    "success": report.success,
                    "recommendations": report.recommendations or [],
                } if report else None,
                "resolution_seconds": _seconds_between(report.started_at, report.completed_at) if report else None,
                "timeline": timeline,
            })
        return audits
    except Exception:
        return _runtime_incidents(limit)
    finally:
        if session is not None:
            session.close()


def get_incident_audit_detail(incident_id: str) -> dict[str, Any] | None:
    return next((item for item in get_incident_audit(limit=500) if item["id"] == incident_id), None)


def get_live_investigation() -> dict[str, Any]:
    """Expose current MAO work without inventing in-progress agent state."""
    kernel = runtime.kernel
    tasks = kernel.state.get_tasks()
    results = kernel.state.agent_results
    result_by_task = {
        result.metadata.get("task_name"): result
        for result in results
        if result.metadata
    }
    stages = []
    for task in tasks[-20:]:
        result = result_by_task.get(task.name)
        stages.append({
            "task": task.name,
            "agent": task.assigned_agent,
            "state": "completed" if result and result.success else "failed" if result else task.status.value.lower(),
            "reasoning": result.summary if result else task.description,
            "evidence": result.evidence if result else [],
            "confidence": result.confidence if result else None,
            "recommendation": (result.recommendations[0] if result and result.recommendations else None),
            "timestamp": _iso(result.timestamp) if result else None,
        })
    latest_report = kernel.state.execution_reports[-1] if kernel.state.execution_reports else None
    completed = sum(stage["state"] == "completed" for stage in stages)
    failed = sum(stage["state"] == "failed" for stage in stages)
    evidence_count = sum(len(stage["evidence"]) for stage in stages)
    started_at = next((stage["timestamp"] for stage in stages if stage["timestamp"]), None)
    return {
        "status": "completed" if latest_report else "waiting",
        "workflow": getattr(latest_report, "workflow_name", None),
        "current_reasoning": getattr(latest_report, "final_summary", "Waiting for an incident investigation."),
        "confidence": getattr(latest_report, "average_confidence", None),
        "current_recommendation": (
            latest_report.recommendations[0]
            if latest_report and latest_report.recommendations else None
        ),
        "approval_required": bool(getattr(latest_report, "approval_required", False)),
        "progress": 100 if latest_report else 0,
        "metadata": {
            "workflow_version": "mao-supervisor-v1",
            "started_at": started_at,
            "agent_count": len(stages),
            "completed_agents": completed,
            "failed_agents": failed,
            "evidence_count": evidence_count,
            "data_freshness": "live_runtime" if stages else "waiting_for_event",
            "recommendation_basis": "agent evidence, safety constraints, prediction, and operational knowledge",
        },
        "stages": stages,
    }


def _notifications() -> list[dict[str, Any]]:
    from services.notification_service import notification_service
    return [{
        "id": notification.id,
        "title": notification.title,
        "message": notification.message,
        "severity": notification.severity.value if hasattr(notification.severity, "value") else str(notification.severity),
        "timestamp": _iso(notification.timestamp),
        "asset_id": notification.asset_id,
        "incident_type": notification.incident_type,
        "human_approval_required": notification.human_approval_required,
    } for notification in notification_service.get_notifications(limit=10)]


def get_execution_reports(limit: int = 100) -> list[dict[str, Any]]:
    """Prefer persisted reports; live MAO state remains an outage fallback."""
    session = None
    try:
        from database.connection import get_session
        from database.models import ExecutionReportDB

        session = get_session()
        records = (
            session.query(ExecutionReportDB)
            .order_by(ExecutionReportDB.completed_at.desc())
            .limit(limit)
            .all()
        )
        if records:
            return [
                {
                    "id": report.id,
                    "workflow": report.workflow,
                    "success": report.success,
                    "summary": report.summary,
                    "recommendations": report.recommendations or [],
                    "started_at": _iso(report.started_at),
                    "completed_at": _iso(report.completed_at),
                    "agent_results": 0,
                    "source": "persistent_audit",
                }
                for report in records
            ]
    except Exception:
        pass
    finally:
        if session is not None:
            session.close()

    return api.get_reports()[-limit:]


def get_operations_live() -> dict[str, Any]:
    """One snapshot for all Operations Center views and WebSocket updates."""
    # Asset health changes continuously in the simulator.  The generic adapter
    # has a cache for list endpoints, but a live control-room snapshot must
    # invalidate it or the WebSocket will keep broadcasting stale health.
    assets = api.get_assets(force_refresh=True)
    audits = get_incident_audit(limit=20)
    activity = api.get_agent_activity(limit=20)
    reports = get_execution_reports(limit=100)
    from api.adapters.maintenance_adapter import get_maintenance_plan
    maintenance = get_maintenance_plan()
    critical_assets = sorted(assets, key=lambda asset: asset.get("health", 100))[:5]
    asset_by_id = {asset.get("id"): asset for asset in assets}
    refinery_groups: dict[str, list[dict[str, Any]]] = {}
    for asset in assets:
        refinery_groups.setdefault(asset.get("location") or "Unassigned", []).append(asset)

    refinery_portfolio = []
    telemetry_by_refinery = []
    for refinery_name, refinery_assets in sorted(refinery_groups.items()):
        refinery_asset_ids = {asset.get("id") for asset in refinery_assets}
        health = round(sum(float(asset.get("health", 0)) for asset in refinery_assets) / len(refinery_assets), 1)
        at_risk = [asset for asset in refinery_assets if float(asset.get("health", 100)) < 80]
        refinery_incidents = [audit for audit in audits if audit.get("asset_id") in refinery_asset_ids]
        focus_asset = min(refinery_assets, key=lambda asset: float(asset.get("health", 100)))
        refinery_history = runtime.kernel.state.get_history(focus_asset.get("id"))[-20:]
        latest_sensor = getattr(refinery_history[-1], "sensor_type", None) if refinery_history else None
        latest_sensor_value = getattr(latest_sensor, "value", latest_sensor)
        readings = [
            {"timestamp": _iso(reading.timestamp), "value": float(reading.value), "sensor_type": getattr(getattr(reading, "sensor_type", None), "value", str(getattr(reading, "sensor_type", ""))), "unit": getattr(reading, "unit", "")}
            for reading in refinery_history
            if getattr(getattr(reading, "sensor_type", None), "value", getattr(reading, "sensor_type", None)) == latest_sensor_value
        ]
        refinery_portfolio.append({
            "name": refinery_name,
            "asset_count": len(refinery_assets),
            "fleet_health": health,
            "assets_at_risk": len(at_risk),
            "open_incidents": sum(audit.get("status") not in ("completed", "resolved") for audit in refinery_incidents),
            "critical_incidents": sum(audit.get("severity") in ("Critical", "High") for audit in refinery_incidents),
            "focus_asset": {"id": focus_asset.get("id"), "name": focus_asset.get("name"), "health": focus_asset.get("health")},
        })
        telemetry_by_refinery.append({
            "refinery": refinery_name,
            "asset_id": focus_asset.get("id"),
            "asset_name": focus_asset.get("name"),
            "sensor_type": latest_sensor_value,
            "unit": readings[-1].get("unit", "") if readings else "",
            "readings": readings,
        })
    telemetry_asset_id = (
        (audits[0].get("asset_id") if audits else None)
        or (critical_assets[0].get("id") if critical_assets else None)
    )
    history = runtime.kernel.state.get_history(telemetry_asset_id) if telemetry_asset_id else []
    latest_sensor = getattr(history[-1], "sensor_type", None) if history else None
    latest_sensor_value = getattr(latest_sensor, "value", latest_sensor)
    telemetry_stream = [
        {
            "timestamp": _iso(reading.timestamp),
            "value": float(reading.value),
            "sensor_type": getattr(reading.sensor_type, "value", str(reading.sensor_type)),
            "unit": getattr(reading, "unit", ""),
        }
        for reading in history
        if getattr(getattr(reading, "sensor_type", None), "value", getattr(reading, "sensor_type", None)) == latest_sensor_value
    ][-60:]
    fleet_health = round(sum(asset.get("health", 0) for asset in assets) / len(assets), 1) if assets else 0
    # This is intentionally a modelled operating-value projection, not booked revenue.
    # The simple health/availability model can later be replaced by a finance feed.
    value_per_asset = 420_000
    base_value = len(assets) * value_per_asset * max(fleet_health, 0) / 100
    revenue_projection = [
        {
            "period": f"P{index + 1}",
            "value": round(base_value * (0.96 + index * 0.012), 2),
        }
        for index in range(8)
    ]
    return {
        "generated_at": datetime.now().isoformat(),
        "dashboard": {
            "total_assets": len(assets),
            "healthy_assets": sum(asset.get("status") == "Running" for asset in assets),
            "fleet_health": fleet_health,
            "active_incidents": sum(audit["status"] not in ("completed", "resolved") for audit in audits),
        },
        "assets": assets,
        "refineries": refinery_portfolio,
        "telemetry_by_refinery": telemetry_by_refinery,
        "telemetry": {
            "asset_id": telemetry_asset_id,
            "asset_name": next((asset.get("name") for asset in assets if asset.get("id") == telemetry_asset_id), "No asset selected"),
            "sensor_type": latest_sensor_value,
            "unit": telemetry_stream[-1].get("unit", "") if telemetry_stream else "",
            "readings": telemetry_stream,
        },
        "critical_incidents": [audit for audit in audits if audit["severity"] in ("Critical", "High")][:5],
        "audit_logs": audits,
        "investigation": get_live_investigation(),
        "ai_activity": activity,
        "maintenance": maintenance,
        "predicted_failures": critical_assets,
        "notifications": _notifications(),
        "reports": reports[-10:],
        "revenue_projection": {
            "kind": "modelled_production_value",
            "currency": "USD",
            "basis": "asset availability and health",
            "periods": revenue_projection,
        },
    }
