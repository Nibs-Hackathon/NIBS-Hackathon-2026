"""Optimized persistence service with async/batch operations."""

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Any
from datetime import datetime

from database.connection import get_session
from database.models import AgentExecutionDB, ExecutionReportDB, IncidentDB, TelemetryDB
from database.repositories.agent_repo import AgentRepository
from database.repositories.incident_repo import IncidentRepository
from database.repositories.report_repo import ReportRepository
from database.repositories.telemetry_repo import TelemetryRepository

logger = logging.getLogger(__name__)

# Thread pool for async persistence
_pool = ThreadPoolExecutor(max_workers=2)


class PersistenceService:
    
    def record_telemetry(self, readings):
        """Async persistence - don't block the main thread."""
        if not readings:
            return
        _pool.submit(self._record_telemetry_sync, readings)

    def _record_telemetry_sync(self, readings):
        """Sync version for background thread."""
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

    def record_execution(self, event, report, severity="high"):
        """Async persistence - don't block the main thread."""
        _pool.submit(self._record_execution_sync, event, report, severity)

    def _record_execution_sync(self, event, report, severity):
        """✅ Sync version for background thread - ADD THIS METHOD."""
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
        except Exception:
            session.rollback()
            logger.exception("Failed to persist MAO execution.")
        finally:
            session.close()

    def wait_for_persistence(self):
        """Wait for all pending persistence operations to complete."""
        _pool.shutdown(wait=True)