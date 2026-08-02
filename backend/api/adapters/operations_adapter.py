"""Read models for the RigOS Operations Center.

This module deliberately composes the existing MAO runtime and persistence
records.  It does not alter agent, simulator, or database behaviour.
"""

from __future__ import annotations

from datetime import datetime
import logging
import os
from threading import Lock
import time
from typing import Any

from api.adapters.backend_api_new import api
from services.runtime import runtime
from services.local_mode import local_demo_mode
from services.refinery_geo import refinery_geo_payload

logger = logging.getLogger(__name__)

# A database outage must not serially delay every HTTP poll and WebSocket tick.
# After one failed durable-store attempt, serve the runtime audit fallback briefly
# before probing persistence again.
_PERSISTENCE_RETRY_AFTER = 0.0
_REPORTS_RETRY_AFTER = 0.0
_REPORTS_CACHE: dict[str, Any] = {"rows": [], "limit": 0, "expires_at": 0.0}
_REPORTS_CACHE_LOCK = Lock()
_REPORTS_CACHE_SECONDS = max(
    5.0,
    float(os.getenv("RIGOS_REPORTS_CACHE_SECONDS", "20")),
)
_PERSISTENCE_BACKOFF_SECONDS = 30.0
_SNAPSHOT_CACHE: dict[str, Any] = {"value": None, "expires_at": 0.0}
_SNAPSHOT_LOCK = Lock()
_SNAPSHOT_CACHE_SECONDS = max(
    1.0,
    float(os.getenv("RIGOS_SNAPSHOT_CACHE_SECONDS", "4")),
)


def _average_asset_health(assets: list[dict[str, Any]]) -> float | None:
    """Average only health readings actually present in the live snapshot."""
    readings = []
    for asset in assets:
        try:
            value = float(asset.get("health"))
        except (TypeError, ValueError):
            continue
        if 0 <= value <= 100:
            readings.append(value)
    return round(sum(readings) / len(readings), 1) if readings else None


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


def _sensor_from_incident(incident_type: str | None) -> str | None:
    normalized = str(incident_type or "").replace("_", "").replace("-", "").lower()
    for marker, sensor in (
        ("pressure", "Pressure"),
        ("temperature", "Temperature"),
        ("vibration", "Vibration"),
        ("gas", "Gas"),
        ("flow", "Flow"),
    ):
        if marker in normalized:
            return sensor
    return None


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
    events = runtime.kernel.event_store.all()
    reports = list(getattr(runtime.kernel.state, "execution_reports", []) or [])
    reports_by_incident = {
        (report.metadata or {}).get("incident_id"): report
        for report in reports
        if (report.metadata or {}).get("incident_id")
    }
    # Reports produced before incident identifiers were added still align with
    # the event store because the kernel appends each pair once per workflow.
    for event, report in zip(events, reports):
        reports_by_incident.setdefault(event.id, report)
    simulator = getattr(runtime, "active_simulator", None)
    active_event_ids = {
        getattr(item.get("event"), "id", None)
        for item in getattr(simulator, "active_incidents", {}).values()
    } if simulator else set()
    resolution_history = getattr(simulator, "incident_resolutions", {}) if simulator else {}

    for event in reversed(events[-limit:]):
        payload = getattr(event, "payload", {}) or {}
        asset = runtime.kernel.asset_service.get(getattr(event, "source", ""))
        report = reports_by_incident.get(event.id)
        report_results = list(getattr(report, "agent_results", []) or [])
        confidence = getattr(report, "average_confidence", None)
        timeline = [{
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
        }]
        timeline.extend(_agent_step(result) for result in report_results)
        resolution = resolution_history.get(str(event.id))
        if resolution:
            timeline.append({
                "id": f"{event.id}-resolved",
                "kind": "resolution",
                "agent": "simulator",
                "title": "Field condition normalized",
                "status": "resolved",
                "timestamp": _iso(resolution.get("resolved_at")),
                "reasoning": (
                    "Safe telemetry or completed linked field work resolved the "
                    "simulated operating condition."
                ),
                "evidence": [],
                "confidence": None,
                "duration_seconds": resolution.get("resolution_seconds"),
                "output": {
                    "health_after": resolution.get("health_after"),
                    "resolution_seconds": resolution.get("resolution_seconds"),
                },
                "recommendations": [],
                "requires_human_approval": False,
            })
        incidents.append({
            "id": event.id,
            "timestamp": _iso(event.timestamp),
            "severity": _severity_from_payload(payload),
            "asset_id": event.source,
            "asset_name": getattr(asset, "name", event.source),
            "facility": getattr(asset, "location", None),
            "incident_type": event.name,
            "status": "active" if event.id in active_event_ids else "resolved",
            "confidence": confidence,
            "health_before": None,
            "health_after": getattr(asset, "health", None),
            "health_capture_status": "not persisted for this runtime event",
            "operator_actions": [],
            "ai_recommendation": (
                report.recommendations[0]
                if report and report.recommendations
                else None
            ),
            "agent_actions": (
                ((report.metadata or {}).get("agent_actuation") or {}).get("executed")
                if report
                else []
            ) or [],
            "execution_report": {
                "id": report.id,
                "summary": report.final_summary,
                "success": report.success,
                "recommendations": report.recommendations or [],
                "confidence": confidence,
                "agent_actions": (
                    ((report.metadata or {}).get("agent_actuation") or {}).get("executed")
                    or []
                ),
            } if report else None,
            "resolution_seconds": resolution.get("resolution_seconds") if resolution else None,
            "resolved_at": _iso(resolution.get("resolved_at")) if resolution else None,
            "timeline": timeline,
        })
    return incidents


def get_incident_audit(limit: int = 100) -> list[dict[str, Any]]:
    """Return durable, incident-centred MAO audit records.

    The database is preferred because runtime EventStore data is intentionally
    ephemeral. A live fallback keeps the control room useful during a database
    outage without presenting it as durable audit history.
    """
    global _PERSISTENCE_RETRY_AFTER
    if local_demo_mode():
        return _runtime_incidents(limit)
    if time.monotonic() < _PERSISTENCE_RETRY_AFTER:
        return _runtime_incidents(limit)
    session = None
    try:
        from database.connection import get_session
        from database.models import ActionDB, AgentExecutionDB, AssetDB, ExecutionReportDB, IncidentDB

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
            if asset is None:
                asset = session.query(AssetDB).filter(AssetDB.id == incident.asset_id).first()
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
                    "status": "completed" if report.success else "requires_review",
                    "timestamp": _iso(report.completed_at),
                    "reasoning": report.summary,
                    "evidence": [],
                    "confidence": None,
                    "duration_seconds": _seconds_between(report.started_at, report.completed_at),
                    "output": report.summary,
                    "recommendations": report.recommendations or [],
                    "requires_human_approval": False,
                })
            if incident.resolved_at:
                timeline.append({
                    "id": f"{incident.id}-resolved",
                    "kind": "resolution",
                    "agent": "simulator",
                    "title": "Field condition normalized",
                    "status": "resolved",
                    "timestamp": _iso(incident.resolved_at),
                    "reasoning": (
                        "The simulator confirmed safe telemetry or an operator-completed "
                        "linked field-work order."
                    ),
                    "evidence": [],
                    "confidence": None,
                    "duration_seconds": incident.resolution_seconds,
                    "output": {
                        "health_after": incident.health_after,
                        "resolution_seconds": incident.resolution_seconds,
                    },
                    "recommendations": [],
                    "requires_human_approval": False,
                })
            timeline.sort(key=lambda item: item["timestamp"] or "")
            confidence_values = [
                float(execution.confidence)
                for execution in executions
                if execution.confidence is not None
            ]
            confidence = (
                round(sum(confidence_values) / len(confidence_values), 4)
                if confidence_values
                else None
            )
            audits.append({
                "id": incident.id,
                "timestamp": _iso(incident.created_at),
                "severity": incident.severity,
                "asset_id": incident.asset_id,
                "asset_name": getattr(asset, "name", incident.asset_id),
                "facility": getattr(asset, "location", None),
                "incident_type": incident.event,
                "status": incident.status,
                "confidence": confidence,
                # Historic before/after health was not captured by the original
                # schema. Never infer it as an audit fact.
                "health_before": incident.health_before,
                "health_after": incident.health_after,
                "health_capture_status": "captured at incident detection and workflow completion" if incident.health_before is not None else "historic record predates outcome snapshots",
                "operator_actions": [_action_step(action) for action in actions],
                "ai_recommendation": (report.recommendations[0] if report and report.recommendations else None),
                "agent_actions": (
                    ((getattr(report, "metadata", None) or {}).get("agent_actuation") or {}).get("executed")
                    if report else []
                ) or [],
                "execution_report": {
                    "id": report.id,
                    "summary": report.summary,
                    "success": report.success,
                    "recommendations": report.recommendations or [],
                    "confidence": confidence,
                    "agent_actions": (
                        ((getattr(report, "metadata", None) or {}).get("agent_actuation") or {}).get("executed")
                        or []
                    ),
                } if report else None,
                "resolution_seconds": incident.resolution_seconds,
                "resolved_at": _iso(incident.resolved_at),
                "timeline": timeline,
            })
        _PERSISTENCE_RETRY_AFTER = 0.0
        return audits
    except Exception:
        _PERSISTENCE_RETRY_AFTER = time.monotonic() + _PERSISTENCE_BACKOFF_SECONDS
        return _runtime_incidents(limit)
    finally:
        if session is not None:
            session.close()


def get_incident_audit_detail(incident_id: str) -> dict[str, Any] | None:
    return next((item for item in get_incident_audit(limit=500) if item["id"] == incident_id), None)


def get_operator_actions(
    limit: int = 50,
    incident_id: str | None = None,
    asset_id: str | None = None,
) -> list[dict[str, Any]]:
    """Return persisted operator actions for audit spine and incident detail."""
    global _PERSISTENCE_RETRY_AFTER
    if time.monotonic() < _PERSISTENCE_RETRY_AFTER:
        return []
    session = None
    try:
        from database.connection import get_session
        from database.models import ActionDB

        session = get_session()
        query = session.query(ActionDB).order_by(ActionDB.created_at.desc())
        if incident_id:
            query = query.filter(ActionDB.incident_id == incident_id)
        if asset_id:
            query = query.filter(ActionDB.asset_id == asset_id)
        records = query.limit(max(1, min(limit, 200))).all()
        actions = []
        for action in records:
            payload = action.payload or {}
            actions.append({
                "id": action.id,
                "incident_id": action.incident_id,
                "asset_id": action.asset_id,
                "action_type": action.action_type,
                "title": action.action_type.replace("_", " ").title(),
                "status": action.status,
                "timestamp": _iso(action.executed_at or action.created_at),
                "approved_by": action.approved_by,
                "operator": action.approved_by or action.requested_by,
                "decision": payload.get("decision"),
                "note": payload.get("note"),
                "payload": payload,
            })
        _PERSISTENCE_RETRY_AFTER = 0.0
        return actions
    except Exception:
        _PERSISTENCE_RETRY_AFTER = time.monotonic() + _PERSISTENCE_BACKOFF_SECONDS
        return []
    finally:
        if session is not None:
            session.close()


def get_live_investigation() -> dict[str, Any]:
    """Expose only the latest workflow's own evidence and agent sequence."""
    kernel = runtime.kernel
    simulator = runtime.active_simulator
    active_incidents = list(getattr(simulator, "active_incidents", {}).values()) if simulator else []
    active_incident = active_incidents[-1] if active_incidents else None
    active_event = active_incident.get("event") if active_incident else None
    latest_report = kernel.state.execution_reports[-1] if kernel.state.execution_reports else None
    report_results = list(getattr(latest_report, "agent_results", []) or [])
    stages = [
        {
            "task": (result.metadata or {}).get("task_name", result.agent_name),
            "agent": result.agent_name,
            "state": "completed" if result.success else "failed",
            "reasoning": result.summary or result.output or result.task,
            "evidence": result.evidence or [],
            "confidence": result.confidence,
            "recommendation": result.recommendations[0] if result.recommendations else None,
            "timestamp": _iso(result.timestamp),
            "duration_seconds": (result.metadata or {}).get("execution_time"),
        }
        for result in report_results
    ]
    completed = sum(stage["state"] == "completed" for stage in stages)
    failed = sum(stage["state"] == "failed" for stage in stages)
    evidence_count = sum(len(stage["evidence"]) for stage in stages)
    started_at = next((stage["timestamp"] for stage in stages if stage["timestamp"]), None)
    return {
        "status": "investigating" if active_incident else ("completed" if latest_report else "waiting"),
        "workflow": getattr(latest_report, "workflow_name", None),
        "current_reasoning": getattr(latest_report, "final_summary", "Waiting for an incident investigation."),
        "confidence": getattr(latest_report, "average_confidence", None),
        "current_recommendation": latest_report.recommendations[0] if latest_report and latest_report.recommendations else None,
        "approval_required": bool(getattr(latest_report, "approval_required", False)),
        "progress": 100 if latest_report else 0,
        "incident": {
            "id": getattr(active_event, "id", None),
            "asset_id": getattr(active_event, "source", None),
            "asset_name": active_incident.get("asset_name") if active_incident else None,
            "incident_type": getattr(active_event, "name", None),
            "detected_at": _iso(active_incident.get("start_time")) if active_incident else None,
            "physical_state": "active" if active_incident else "no_active_incident",
        },
        "metadata": {
            "workflow_version": "mao-supervisor-v1",
            "started_at": started_at,
            "agent_count": len(stages),
            "completed_agents": completed,
            "failed_agents": failed,
            "evidence_count": evidence_count,
            "data_freshness": "latest_completed_workflow" if stages else "waiting_for_event",
            "recommendation_basis": "agent evidence, safety constraints, prediction, and operational knowledge",
            "operational_state": "field condition remains active" if active_incident else "no active field incident",
        },
        "stages": stages,
    }


def _notifications() -> list[dict[str, Any]]:
    from services.notification_service import notification_service
    return [{
        "id": notification.id,
        "type": notification.type.value if hasattr(notification.type, "value") else str(notification.type),
        "title": notification.title,
        "message": notification.message,
        "severity": notification.severity.value if hasattr(notification.severity, "value") else str(notification.severity),
        "timestamp": _iso(notification.timestamp),
        "asset_id": notification.asset_id,
        "asset_name": notification.asset_name,
        "refinery_name": getattr(notification, "refinery_name", None),
        "incident_type": notification.incident_type,
        "revenue_impact": notification.revenue_impact,
        "metadata": notification.metadata,
        "read": notification.read,
        "human_approval_required": notification.human_approval_required,
    } for notification in notification_service.get_notifications(limit=50)]


def get_execution_reports(limit: int = 100) -> list[dict[str, Any]]:
    """Merge persisted and live reports so a generated brief is never hidden."""
    global _REPORTS_RETRY_AFTER
    if local_demo_mode():
        return api.get_reports(force_refresh=True)[-limit:]
    now = time.monotonic()
    with _REPORTS_CACHE_LOCK:
        cached_rows = list(_REPORTS_CACHE["rows"])
        cached_limit = int(_REPORTS_CACHE["limit"])
        cache_valid = (
            cached_rows
            and cached_limit >= limit
            and now < float(_REPORTS_CACHE["expires_at"])
        )
    if cache_valid:
        live_reports = api.get_reports(force_refresh=True)
        merged = {str(row.get("id")): row for row in cached_rows if row.get("id")}
        for row in live_reports:
            report_id = str(row.get("id") or "")
            if report_id:
                merged[report_id] = {**row, **merged.get(report_id, {})}
        return sorted(
            merged.values(),
            key=lambda row: str(row.get("completed_at") or row.get("created_at") or row.get("started_at") or ""),
        )[-limit:]
    if time.monotonic() < _REPORTS_RETRY_AFTER:
        return api.get_reports(force_refresh=True)[-limit:]
    session = None
    try:
        from database.connection import get_session
        from database.models import ActionDB, AgentExecutionDB, AssetDB, ExecutionReportDB, IncidentDB

        session = get_session()
        records = (
            session.query(ExecutionReportDB)
            .order_by(ExecutionReportDB.completed_at.desc())
            .limit(limit)
            .all()
        )
        reports = []
        if records:
            # Batch the remote PostgreSQL reads. The old per-report lookup made
            # roughly four tunnel round trips for every brief, which was slow
            # enough to trigger the live-memory fallback on a TCP tunnel.
            incident_ids = {
                report.incident_id for report in records if report.incident_id
            }
            incident_rows = (
                session.query(IncidentDB)
                .filter(IncidentDB.id.in_(incident_ids))
                .all()
                if incident_ids else []
            )
            incidents_by_id = {incident.id: incident for incident in incident_rows}
            execution_rows = (
                session.query(AgentExecutionDB)
                .filter(AgentExecutionDB.incident_id.in_(incident_ids))
                .all()
                if incident_ids else []
            )
            action_rows = (
                session.query(ActionDB)
                .filter(ActionDB.incident_id.in_(incident_ids))
                .all()
                if incident_ids else []
            )
            executions_by_incident: dict[str, list[Any]] = {}
            for execution in execution_rows:
                executions_by_incident.setdefault(execution.incident_id, []).append(execution)
            actions_by_incident: dict[str, list[Any]] = {}
            for action in action_rows:
                actions_by_incident.setdefault(action.incident_id, []).append(action)
            asset_ids = {
                incident.asset_id for incident in incident_rows if incident.asset_id
            }
            database_assets = (
                session.query(AssetDB)
                .filter(AssetDB.id.in_(asset_ids))
                .all()
                if asset_ids else []
            )
            database_assets_by_id = {asset.id: asset for asset in database_assets}

            # Normalize to the same oldest-to-newest order as live MAO state.
            for report in reversed(records):
                incident = incidents_by_id.get(report.incident_id)
                executions = executions_by_incident.get(report.incident_id, [])
                actions = actions_by_incident.get(report.incident_id, [])
                asset = runtime.kernel.asset_service.get(incident.asset_id) if incident else None
                if asset is None and incident:
                    asset = database_assets_by_id.get(incident.asset_id)
                confidence_values = [
                    float(execution.confidence)
                    for execution in executions
                    if execution.confidence is not None
                ]
                confidence = (
                    round(sum(confidence_values) / len(confidence_values), 4)
                    if confidence_values
                    else None
                )
                diagnostic = next(
                    (execution for execution in executions if execution.agent_name == "diagnostic"),
                    None,
                )
                economics = {}
                if incident and asset:
                    try:
                        from services.revenue_impact_calculator import revenue_service
                        asset_type = getattr(
                            getattr(asset, "asset_type", None),
                            "value",
                            getattr(asset, "asset_type", "Unknown"),
                        )
                        economics = revenue_service.calculate_incident_impact(
                            incident.event,
                            str(asset_type),
                            duration_hours=2,
                        )
                    except Exception:
                        economics = {}
                board_actions = [
                    action for action in actions
                    if action.action_type in {"board_approve", "board_defer", "board_escalate"}
                    and (
                        not (action.payload or {}).get("report_id")
                        or str((action.payload or {}).get("report_id")) == str(report.id)
                    )
                ]
                board_action = max(
                    board_actions,
                    key=lambda action: action.created_at or datetime.min,
                    default=None,
                )
                board_payload = (board_action.payload or {}) if board_action else {}
                board_labels = {
                    "approved": "Approved for publication",
                    "deferred": "Deferred pending revision",
                    "escalated": "Escalated to operating committee",
                }
                board_decision = board_payload.get("decision") if board_action else None
                board_status = board_labels.get(board_decision, "Awaiting board approval")
                recommendation = (report.recommendations or [None])[0]
                timeline = [
                    {
                        "event": "Signal detected",
                        "detail": "Case opened in the operating record",
                        "when": _iso(report.started_at),
                    },
                    {
                        "event": "Investigation completed",
                        "detail": "AI evidence package closed",
                        "when": _iso(report.completed_at),
                    },
                ]
                if recommendation:
                    timeline.append({
                        "event": "Recommendation prepared",
                        "detail": str(recommendation)[:120],
                        "when": _iso(report.completed_at),
                    })
                if board_action:
                    timeline.append({
                        "event": "Board decision",
                        "detail": board_status,
                        "when": _iso(board_action.executed_at or board_action.created_at),
                    })
                reports.append({
                    "id": report.id,
                    "incident_id": report.incident_id,
                    "title": f"{incident.event} executive brief" if incident else "Operational executive brief",
                    "workflow": report.workflow,
                    "success": report.success,
                    "status": "completed" if report.success else "requires_review",
                    "summary": report.summary,
                    "executive_summary": report.summary,
                    "confidence": confidence,
                    "root_cause": (
                        getattr(diagnostic, "output", None)
                        or getattr(diagnostic, "summary", None)
                    ),
                    "financial_impact": economics.get("revenue_loss"),
                    "maintenance_cost": economics.get("maintenance_cost"),
                    "production_impact": economics.get("production_impact_pct"),
                    "economics_provenance": economics.get("provenance"),
                    "recommendations": report.recommendations or [],
                    "recommendation": recommendation,
                    "timeline": timeline,
                    "started_at": _iso(report.started_at),
                    "completed_at": _iso(report.completed_at),
                    "duration_seconds": _seconds_between(report.started_at, report.completed_at),
                    "asset_id": incident.asset_id if incident else None,
                    "asset_name": getattr(asset, "name", incident.asset_id) if incident else None,
                    "facility": getattr(asset, "location", None),
                    "incident_type": incident.event if incident else None,
                    "incident_status": incident.status if incident else "unlinked",
                    "agent_results": len(executions),
                    "agents": [execution.agent_name for execution in executions],
                    "failed_agents": [execution.agent_name for execution in executions if not execution.success],
                    "operator_actions": len(actions),
                    "board_decision": board_decision,
                    "board_status": board_status,
                    "board_decision_at": (
                        _iso(board_action.executed_at or board_action.created_at)
                        if board_action else None
                    ),
                    "board_decision_by": (
                        board_action.approved_by
                        or board_action.requested_by
                        if board_action else None
                    ),
                    "board_rationale": board_payload.get("note"),
                    "source": "persistent_audit",
                })
        live_reports = api.get_reports(force_refresh=True)
        merged = {str(row.get("id")): row for row in reports if row.get("id")}
        for row in live_reports:
            report_id = str(row.get("id") or "")
            if not report_id:
                continue
            merged[report_id] = {**row, **merged.get(report_id, {})}
        with _REPORTS_CACHE_LOCK:
            _REPORTS_CACHE.update({
                "rows": list(reports),
                "limit": limit,
                "expires_at": time.monotonic() + _REPORTS_CACHE_SECONDS,
            })
        _REPORTS_RETRY_AFTER = 0.0
        return sorted(
            merged.values(),
            key=lambda row: str(row.get("completed_at") or row.get("created_at") or row.get("started_at") or ""),
        )[-limit:]
    except Exception as error:
        _REPORTS_RETRY_AFTER = time.monotonic() + _PERSISTENCE_BACKOFF_SECONDS
        logger.warning(
            "Persistent execution reports unavailable; serving live runtime reports: %s",
            error,
        )
    finally:
        if session is not None:
            session.close()

    return api.get_reports(force_refresh=True)[-limit:]


def invalidate_execution_report_cache() -> None:
    """Make a persisted board action visible on the next report read."""
    with _REPORTS_CACHE_LOCK:
        _REPORTS_CACHE.update({"rows": [], "limit": 0, "expires_at": 0.0})


def get_execution_report_export(report_id: str, fmt: str = "markdown") -> dict[str, Any]:
    """Return an honest export package (markdown or JSON) for a report — not a PDF blob."""
    reports = get_execution_reports(limit=200)
    report = next((row for row in reports if str(row.get("id")) == str(report_id)), None)
    if report is None:
        # Fallback: live MAO reports may use different id shapes
        for row in api.get_reports():
            if str(row.get("id")) == str(report_id):
                report = row
                break
    if report is None:
        raise LookupError(f"Report {report_id} not found")

    title = report.get("title") or report.get("name") or report.get("incident_type") or f"Report {report_id}"
    summary = report.get("summary") or report.get("executive_summary") or "No summary recorded."
    recommendations = report.get("recommendations") or []
    if isinstance(recommendations, str):
        recommendations = [recommendations]
    production_impact = report.get("production_impact")
    production_impact_display = (
        f"{production_impact}%"
        if production_impact is not None
        else "not available"
    )

    markdown_lines = [
        f"# {title}",
        "",
        f"- Report ID: `{report.get('id')}`",
        f"- Incident ID: `{report.get('incident_id') or 'unlinked'}`",
        f"- Asset: {report.get('asset_name') or report.get('asset_id') or 'n/a'}",
        f"- Status: {report.get('status') or ('completed' if report.get('success') else 'requires_review')}",
        f"- Completed: {report.get('completed_at') or report.get('created_at') or 'n/a'}",
        "",
        "## Executive summary",
        summary,
        "",
        "## Operating impact",
        f"- Modeled exposure: {report.get('financial_impact') if report.get('financial_impact') is not None else 'not available'}",
        f"- Estimated maintenance cost: {report.get('maintenance_cost') if report.get('maintenance_cost') is not None else 'not available'}",
        f"- Estimated production impact: {production_impact_display}",
        f"- Root cause: {report.get('root_cause') or 'not established'}",
        "",
        "## Recommendations",
    ]
    if recommendations:
        markdown_lines.extend(f"- {item}" for item in recommendations)
    else:
        markdown_lines.append("- None recorded")
    markdown_lines.extend([
        "",
        "## Provenance",
        f"- Source: {report.get('source') or 'operations'}",
        f"- Agents: {', '.join(report.get('agents') or []) or 'n/a'}",
        f"- Operator actions: {report.get('operator_actions', 0)}",
        f"- Board status: {report.get('board_status') or 'Awaiting board approval'}",
        f"- Board decision at: {report.get('board_decision_at') or 'not recorded'}",
        "",
        "_Export package generated by RigOS. This is markdown/JSON — not a rendered PDF._",
    ])
    markdown = "\n".join(markdown_lines)
    return {
        "id": report.get("id"),
        "format": "markdown" if fmt != "json" else "json",
        "filename": f"rigos-report-{report.get('id')}.{'md' if fmt != 'json' else 'json'}",
        "content": markdown if fmt != "json" else report,
        "markdown": markdown,
        "report": report,
        "message": "Export package ready. True PDF rendering is deferred.",
    }


def _build_operations_live() -> dict[str, Any]:
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
    open_audits = [
        audit
        for audit in audits
        if audit.get("status") not in ("completed", "resolved")
    ]
    asset_by_id = {asset.get("id"): asset for asset in assets}
    priority_ids = [
        audit.get("asset_id")
        for audit in open_audits
        if audit.get("asset_id") in asset_by_id
    ]
    priority_ids.extend(
        asset.get("id")
        for asset in sorted(assets, key=lambda item: float(item.get("health", 100)))
    )
    critical_assets = []
    for asset_id in priority_ids:
        if asset_id and all(item.get("id") != asset_id for item in critical_assets):
            critical_assets.append(asset_by_id[asset_id])
        if len(critical_assets) == 8:
            break
    critical_asset_telemetry = []
    for asset in critical_assets:
        asset_history = runtime.kernel.state.get_history(asset.get("id"))[-60:]
        active_audit = next(
            (audit for audit in open_audits if audit.get("asset_id") == asset.get("id")),
            None,
        )
        latest_sensor = getattr(asset_history[-1], "sensor_type", None) if asset_history else None
        sensor_value = (
            _sensor_from_incident(active_audit.get("incident_type"))
            if active_audit
            else getattr(latest_sensor, "value", latest_sensor)
        )
        readings = [
            {"timestamp": _iso(reading.timestamp), "value": float(reading.value), "sensor_type": getattr(getattr(reading, "sensor_type", None), "value", str(getattr(reading, "sensor_type", ""))), "unit": getattr(reading, "unit", "")}
            for reading in asset_history
            if getattr(getattr(reading, "sensor_type", None), "value", getattr(reading, "sensor_type", None)) == sensor_value
        ]
        health_history = []
        if len(asset_history) >= 4:
            stride = max(1, len(asset_history) // 10)
            for index in range(stride, len(asset_history) + 1, stride):
                health_history.append(round(runtime.kernel.health.calculate_health(asset_history[:index]), 1))
        raw_health = asset.get("health")
        current_health = float(raw_health) if raw_health is not None else (health_history[-1] if health_history else None)
        observed_slope = (health_history[-1] - health_history[0]) / max(len(health_history) - 1, 1) if len(health_history) > 1 else 0
        projected_health = [round(max(0, min(100, current_health + observed_slope * period)), 1) for period in range(1, 8)] if current_health is not None and len(health_history) > 1 else []
        critical_asset_telemetry.append({"asset_id": asset.get("id"), "asset_name": asset.get("name"), "sensor_type": sensor_value, "unit": readings[-1].get("unit", "") if readings else "", "readings": readings, "health_history": health_history, "data_available": bool(readings or health_history), "forecast": {"method": "recent telemetry health slope" if projected_health else "unavailable: insufficient health history", "projected_health": projected_health, "slope_per_window": round(observed_slope, 2) if len(health_history) > 1 else None}})
    refinery_groups: dict[str, list[dict[str, Any]]] = {}
    for asset in assets:
        refinery_groups.setdefault(asset.get("location") or "Unassigned", []).append(asset)

    refinery_portfolio = []
    telemetry_by_refinery = []
    for refinery_name, refinery_assets in sorted(refinery_groups.items()):
        refinery_asset_ids = {asset.get("id") for asset in refinery_assets}
        health = _average_asset_health(refinery_assets)
        at_risk = [asset for asset in refinery_assets if float(asset.get("health", 100)) < 80]
        refinery_incidents = [audit for audit in audits if audit.get("asset_id") in refinery_asset_ids]
        focus_asset = min(refinery_assets, key=lambda asset: float(asset.get("health", 100)))
        refinery_history = runtime.kernel.state.get_history(focus_asset.get("id"))[-20:]
        # Temperature is the default portfolio series; incident-specific
        # endpoints still select the affected sensor.
        latest_sensor_value = "Temperature" if refinery_history else None
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
            "sensor_profile_source": (focus_asset.get("metadata") or {}).get("sensor_profile_source"),
            **refinery_geo_payload(refinery_name),
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
        (open_audits[0].get("asset_id") if open_audits else None)
        or (critical_assets[0].get("id") if critical_assets else None)
    )
    history = runtime.kernel.state.get_history(telemetry_asset_id) if telemetry_asset_id else []
    latest_sensor = getattr(history[-1], "sensor_type", None) if history else None
    telemetry_audit = next(
        (audit for audit in open_audits if audit.get("asset_id") == telemetry_asset_id),
        None,
    )
    latest_sensor_value = (
        _sensor_from_incident(telemetry_audit.get("incident_type"))
        if telemetry_audit
        else ("Temperature" if history else getattr(latest_sensor, "value", latest_sensor))
    )
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
    fleet_health = _average_asset_health(assets)
    # This is intentionally a modelled operating-value projection, not booked revenue.
    # The simple health/availability model can later be replaced by a finance feed.
    value_per_asset = 420_000
    base_value = len(assets) * value_per_asset * max(fleet_health or 0, 0) / 100
    revenue_projection = [
        {
            "period": f"P{index + 1}",
            "value": round(base_value * (0.96 + index * 0.012), 2),
        }
        for index in range(8)
    ]
    telemetry_by_asset = {item["asset_id"]: item for item in critical_asset_telemetry}
    predicted_failures = []
    for asset in critical_assets:
        stream = telemetry_by_asset.get(asset.get("id"), {})
        health = asset.get("health")
        projected = stream.get("forecast", {}).get("projected_health", [])
        predicted_failures.append({
            **asset,
            "forecast_available": bool(projected),
            "forecast_method": stream.get("forecast", {}).get("method"),
            "projected_health": projected,
            "risk_score": round(max(0, min(100, 100 - float(health))) if health is not None else 0, 1),
        })
    return {
        "generated_at": datetime.now().isoformat(),
        "dashboard": {
            "total_assets": len(assets),
            "healthy_assets": sum(asset.get("status") == "Running" for asset in assets),
            "fleet_health": fleet_health,
            "active_incidents": sum(audit["status"] not in ("completed", "resolved") for audit in audits),
            "knowledge_documents": getattr(runtime.kernel, "_knowledge_document_count", 0),
            "knowledge_source": getattr(runtime.kernel, "_knowledge_source", "unavailable"),
            "sensor_profile_source": next(
                (
                    (asset.get("metadata") or {}).get("sensor_profile_source")
                    for asset in assets
                    if (asset.get("metadata") or {}).get("sensor_profile_source")
                ),
                "unknown",
            ),
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
        "critical_asset_telemetry": critical_asset_telemetry,
        "critical_incidents": [audit for audit in audits if audit["severity"] in ("Critical", "High")][:5],
        "audit_logs": audits,
        "operator_actions": get_operator_actions(limit=50),
        "investigation": get_live_investigation(),
        "ai_activity": activity,
        "maintenance": maintenance,
        "predicted_failures": predicted_failures,
        "notifications": _notifications(),
        "reports": reports,
        "simulation": dict(getattr(runtime.kernel, "_simulation_stats", {}) or {}),
        "revenue_projection": {
            "kind": "modelled_production_value",
            "currency": "USD",
            "basis": "asset availability and health",
            "periods": revenue_projection,
        },
    }


def get_operations_live() -> dict[str, Any]:
    """Share one bounded snapshot build across REST and all WebSocket clients."""
    now = time.monotonic()
    cached = _SNAPSHOT_CACHE["value"]
    if cached is not None and now < _SNAPSHOT_CACHE["expires_at"]:
        return cached

    with _SNAPSHOT_LOCK:
        now = time.monotonic()
        cached = _SNAPSHOT_CACHE["value"]
        if cached is not None and now < _SNAPSHOT_CACHE["expires_at"]:
            return cached
        snapshot = _build_operations_live()
        _SNAPSHOT_CACHE["value"] = snapshot
        _SNAPSHOT_CACHE["expires_at"] = now + _SNAPSHOT_CACHE_SECONDS
        return snapshot


def invalidate_operations_snapshot() -> None:
    """Make the next read rebuild immediately after an operator mutation."""
    with _SNAPSHOT_LOCK:
        _SNAPSHOT_CACHE["value"] = None
        _SNAPSHOT_CACHE["expires_at"] = 0.0
