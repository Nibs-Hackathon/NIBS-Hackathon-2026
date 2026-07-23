"""Repository-backed persistence for simulator and MAO lifecycle data."""

import logging

from database.connection import get_session
from database.models import (
    ActionDB,
    ActivityEventDB,
    AgentExecutionDB,
    ExecutionReportDB,
    IncidentDB,
    MaintenanceTaskDB,
    NotificationDB,
    PredictionDB,
    TelemetryDB,
)
from database.repositories.action_repo import ActionRepository
from database.repositories.activity_repo import ActivityRepository
from database.repositories.agent_repo import AgentRepository
from database.repositories.incident_repo import IncidentRepository
from database.repositories.maintenance_task_repo import MaintenanceTaskRepository
from database.repositories.notification_repo import NotificationRepository
from database.repositories.prediction_repo import PredictionRepository
from database.repositories.report_repo import ReportRepository
from database.repositories.telemetry_repo import TelemetryRepository


logger = logging.getLogger(__name__)


class PersistenceService:

    def record_telemetry(self, readings):
        session = get_session()
        try:
            rows = [
                TelemetryDB(
                    asset_id=reading.asset_id,
                    sensor_type=reading.sensor_type.value,
                    value=reading.value,
                    timestamp=reading.timestamp,
                )
                for reading in readings
            ]
            TelemetryRepository(session).create_many(rows)
        except Exception:
            session.rollback()
            logger.exception("Failed to persist telemetry batch.")
        finally:
            session.close()

    def record_execution(self, event, report, tasks=None, severity="high"):
        session = get_session()
        try:
            incident = IncidentDB(
                id=event.id,
                asset_id=event.source,
                event=event.name,
                severity=severity,
                status="completed" if report.success else "requires_review",
                report=report.final_summary,
                created_at=event.timestamp,
            )
            IncidentRepository(session).create(incident)

            stored_report = ExecutionReportDB(
                id=report.id,
                execution_id=report.execution_id,
                incident_id=event.id,
                workflow=report.workflow_name,
                success=report.success,
                summary=report.final_summary,
                recommendations=report.recommendations,
                started_at=report.started_at,
                completed_at=report.completed_at,
            )
            ReportRepository(session).create(stored_report)

            agent_rows = [
                AgentExecutionDB(
                    id=result.id,
                    incident_id=event.id,
                    agent_name=result.agent_name,
                    task=result.metadata.get("task_name", ""),
                    input=result.metadata.get("task_description", ""),
                    output=result.summary,
                    success=result.success,
                    confidence=result.confidence,
                    summary=result.summary,
                    recommendations=result.recommendations,
                    decision=result.decision,
                    evidence=result.evidence,
                    actions_required=result.actions_required,
                    requires_human_approval=result.requires_human_approval,
                    timestamp=result.timestamp,
                )
                for result in report.agent_results
            ]
            if agent_rows:
                AgentRepository(session).create_many(agent_rows)

            ActivityRepository(session).create_many(
                [
                    ActivityEventDB(
                        incident_id=event.id,
                        source=result.agent_name,
                        status="completed" if result.success else "failed",
                        summary=result.summary or result.finding,
                        evidence=result.evidence,
                        confidence=result.confidence,
                        created_at=result.timestamp,
                    )
                    for result in report.agent_results
                ]
            )

            ActionRepository(session).create_many(
                [
                    ActionDB(
                        incident_id=event.id,
                        asset_id=event.source,
                        action_type=result.required_action or "operator_review",
                        payload={
                            "agent_result_id": result.id,
                            "recommendations": result.recommendations,
                        },
                        risk_level=report.incident_severity,
                        status="pending_approval",
                        requires_human_approval=True,
                    )
                    for result in report.agent_results
                    if result.requires_human_approval
                ]
            )

            PredictionRepository(session).create_many(
                [
                    PredictionDB(
                        execution_id=report.execution_id,
                        agent_result_id=result.id,
                        asset_id=result.metadata.get("asset_id", event.source),
                        health=result.metadata["health"],
                        failure_probability=result.metadata["failure_probability"],
                        rul_days=result.metadata["rul_days"],
                        confidence=result.metadata["confidence"],
                        evidence=result.metadata.get("evidence", []),
                        created_at=result.timestamp,
                    )
                    for result in report.agent_results
                    if result.agent_name == "prediction"
                ]
            )

            NotificationRepository(session).create_many(
                [
                    NotificationDB(
                        id=notification["id"],
                        execution_id=report.execution_id,
                        asset_id=notification.get("asset_id", event.source),
                        source=notification["source"],
                        severity=notification["severity"],
                        summary=notification["summary"],
                        status="pending_acknowledgement",
                        requires_human_approval=notification.get(
                            "requires_human_approval", False
                        ),
                        details=notification.get("metadata", {}),
                        created_at=notification.get("created_at"),
                    )
                    for result in report.agent_results
                    if result.agent_name == "notification"
                    for notification in result.metadata.get("notifications", [])
                ]
            )

            MaintenanceTaskRepository(session).create_many(
                [
                    MaintenanceTaskDB(
                        id=task.id,
                        execution_id=report.execution_id,
                        incident_id=event.id,
                        asset_id=event.source,
                        name=task.name,
                        description=task.description,
                        assigned_agent=task.assigned_agent,
                        priority=task.priority,
                        status=task.status.value,
                        input_data=task.input_data,
                        output_data=task.output_data,
                        created_at=event.timestamp,
                    )
                    for task in (tasks or [])
                ]
            )
        except Exception:
            session.rollback()
            logger.exception("Failed to persist MAO execution.")
        finally:
            session.close()
