"""Production read API backed by the shared RigOS runtime and repositories."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Callable

from fastapi import FastAPI, HTTPException, Query

from database.connection import get_session
from database.repositories.activity_repo import ActivityRepository
from database.repositories.maintenance_task_repo import MaintenanceTaskRepository
from database.repositories.notification_repo import NotificationRepository
from database.repositories.prediction_repo import PredictionRepository
from database.repositories.report_repo import ReportRepository
from services.runtime import kernel


app = FastAPI(
    title="RigOS Production API",
    version="1.0.0",
    description="Read-only operational state and persisted MAO intelligence outputs.",
)


def _value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _value(item) for key, item in value.items()}
    return value


def _read_repository(loader: Callable) -> list:
    session = None
    try:
        session = get_session()
        return loader(session)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="Persisted operational data is temporarily unavailable.",
        ) from error
    finally:
        if session is not None:
            session.close()


@app.get("/health", tags=["service"])
def health() -> dict:
    """Return the API service health without creating a new MAO runtime."""
    return {"status": "ok", "registered_agents": len(kernel.registry.all())}


@app.get("/api/assets", tags=["operations"])
def get_assets() -> list[dict]:
    return [
        {
            "id": asset.id,
            "name": asset.name,
            "asset_type": _value(asset.asset_type),
            "location": asset.location,
            "health": asset.health,
            "status": asset.status,
        }
        for asset in kernel.asset_service.all_assets()
    ]


@app.get("/api/telemetry", tags=["operations"])
def get_telemetry(asset_id: str | None = Query(default=None)) -> list[dict]:
    asset_ids = [asset_id] if asset_id else list(kernel.state.telemetry.keys())
    return [
        {
            "id": reading.id,
            "asset_id": reading.asset_id,
            "sensor_type": _value(reading.sensor_type),
            "value": reading.value,
            "unit": reading.unit,
            "timestamp": _value(reading.timestamp),
        }
        for current_asset_id in asset_ids
        for reading in kernel.state.get_history(current_asset_id)
    ]


@app.get("/api/incidents", tags=["operations"])
def get_incidents() -> list[dict]:
    return [
        {
            "id": event.id,
            "name": event.name,
            "source": event.source,
            "payload": _value(event.payload),
            "timestamp": _value(event.timestamp),
        }
        for event in kernel.event_store.all()
    ]


@app.get("/api/reports", tags=["intelligence"])
def get_reports(limit: int = Query(default=100, ge=1, le=500)) -> list[dict]:
    reports = _read_repository(lambda session: ReportRepository(session).get_recent(limit))
    return [
        {
            "id": report.id,
            "execution_id": report.execution_id,
            "incident_id": report.incident_id,
            "workflow": report.workflow,
            "success": report.success,
            "summary": report.summary,
            "recommendations": _value(report.recommendations),
            "started_at": _value(report.started_at),
            "completed_at": _value(report.completed_at),
        }
        for report in reports
    ]


@app.get("/api/knowledge", tags=["knowledge"])
def get_knowledge(query: str | None = Query(default=None, min_length=1)) -> list[dict]:
    """Search through the registered Neon-backed KnowledgeAgent retriever."""
    if query is None:
        return []
    agent = kernel.registry.get("knowledge")
    if agent is None or agent.retriever is None:
        raise HTTPException(status_code=503, detail="Knowledge retrieval is unavailable.")
    try:
        documents = agent.retriever.retrieve(query.strip())
    except Exception as error:
        raise HTTPException(status_code=503, detail="Knowledge search could not be completed.") from error
    return [
        {
            "content": document.page_content,
            "metadata": _value(document.metadata or {}),
        }
        for document in documents
    ]


@app.get("/api/agents", tags=["intelligence"])
def get_agents() -> list[dict]:
    latest_results = {
        result.agent_name: result for result in kernel.state.agent_results
    }
    return [
        {
            "name": agent.name,
            "type": agent.__class__.__name__,
            "latest_result": (
                {
                    "success": latest_results[agent.name].success,
                    "summary": latest_results[agent.name].summary,
                    "confidence": latest_results[agent.name].confidence,
                    "timestamp": _value(latest_results[agent.name].timestamp),
                }
                if agent.name in latest_results
                else None
            ),
        }
        for agent in kernel.registry.all()
    ]


@app.get("/api/activity", tags=["intelligence"])
def get_activity(limit: int = Query(default=200, ge=1, le=500)) -> list[dict]:
    activity = _read_repository(lambda session: ActivityRepository(session).get_recent(limit))
    return [
        {
            "id": event.id,
            "incident_id": event.incident_id,
            "source": event.source,
            "status": event.status,
            "summary": event.summary,
            "evidence": _value(event.evidence),
            "confidence": event.confidence,
            "created_at": _value(event.created_at),
        }
        for event in activity
    ]


@app.get("/api/predictions", tags=["intelligence"])
def get_predictions(
    asset_id: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[dict]:
    predictions = _read_repository(
        lambda session: (
            PredictionRepository(session).get_by_asset(asset_id, limit)
            if asset_id
            else PredictionRepository(session).get_recent(limit)
        )
    )
    return [
        {
            "id": prediction.id,
            "execution_id": prediction.execution_id,
            "asset_id": prediction.asset_id,
            "health": prediction.health,
            "failure_probability": prediction.failure_probability,
            "rul_days": prediction.rul_days,
            "confidence": prediction.confidence,
            "evidence": _value(prediction.evidence),
            "created_at": _value(prediction.created_at),
        }
        for prediction in predictions
    ]


@app.get("/api/notifications", tags=["intelligence"])
def get_notifications(limit: int = Query(default=100, ge=1, le=500)) -> list[dict]:
    notifications = _read_repository(
        lambda session: NotificationRepository(session).get_recent(limit)
    )
    return [
        {
            "id": notification.id,
            "execution_id": notification.execution_id,
            "asset_id": notification.asset_id,
            "source": notification.source,
            "severity": notification.severity,
            "summary": notification.summary,
            "status": notification.status,
            "requires_human_approval": notification.requires_human_approval,
            "metadata": _value(notification.details),
            "created_at": _value(notification.created_at),
            "acknowledged_at": _value(notification.acknowledged_at),
            "acknowledged_by": notification.acknowledged_by,
        }
        for notification in notifications
    ]


@app.get("/api/maintenance", tags=["operations"])
def get_maintenance(
    asset_id: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
) -> list[dict]:
    tasks = _read_repository(
        lambda session: (
            MaintenanceTaskRepository(session).get_by_asset(asset_id, limit)
            if asset_id
            else MaintenanceTaskRepository(session).get_recent(limit)
        )
    )
    return [
        {
            "id": task.id,
            "execution_id": task.execution_id,
            "incident_id": task.incident_id,
            "asset_id": task.asset_id,
            "name": task.name,
            "description": task.description,
            "assigned_agent": task.assigned_agent,
            "priority": task.priority,
            "status": task.status,
            "input_data": _value(task.input_data),
            "output_data": _value(task.output_data),
            "created_at": _value(task.created_at),
        }
        for task in tasks
    ]
