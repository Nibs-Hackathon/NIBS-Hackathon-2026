"""Persistence service with buffer and sync saving."""

import logging
import time
from threading import Lock, Thread
from collections import deque
from datetime import datetime
from typing import List, Any

from database.connection import get_session
from database.models import AgentExecutionDB, ExecutionReportDB, IncidentDB, TelemetryDB
from database.repositories.agent_repo import AgentRepository
from database.repositories.incident_repo import IncidentRepository
from database.repositories.report_repo import ReportRepository
from database.repositories.telemetry_repo import TelemetryRepository

logger = logging.getLogger(__name__)


class PersistenceService:
    """Handles database persistence with buffer and sync saving."""
    
    def __init__(self):
        self._buffer = deque(maxlen=5000)  # Buffer up to 5000 readings
        self._lock = Lock()
        self._running = True
        self._flush_thread = None
        self._start_flush_thread()
    
    def _start_flush_thread(self):
        """Start background thread to flush buffer."""
        self._flush_thread = Thread(target=self._flush_loop, daemon=True)
        self._flush_thread.start()
    
    def _flush_loop(self):
        """Background loop to flush buffer every 5 seconds."""
        while self._running:
            time.sleep(5)
            self._flush_buffer()
    
    def _flush_buffer(self):
        """Flush buffered telemetry to database."""
        if not self._buffer:
            return
        
        with self._lock:
            # Get all items from buffer
            items = list(self._buffer)
            self._buffer.clear()
        
        if not items:
            return
        
        # Save in batches
        batch_size = 100
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            self._save_telemetry_sync(batch)
    
    def record_telemetry(self, readings):
        """Add telemetry to buffer (non-blocking)."""
        if not readings:
            return
        
        with self._lock:
            for reading in readings:
                self._buffer.append(reading)
    
    def _save_telemetry_sync(self, readings):
        """Save telemetry to database synchronously."""
        if not readings:
            return
        
        session = None
        try:
            session = get_session()
            if session is None:
                return
            
            rows = [
                TelemetryDB(
                    asset_id=reading.asset_id,
                    sensor_type=reading.sensor_type.value if hasattr(reading.sensor_type, 'value') else str(reading.sensor_type),
                    value=float(reading.value) if hasattr(reading, 'value') else 0,
                    timestamp=getattr(reading, 'timestamp', datetime.now()),
                )
                for reading in readings
            ]
            
            TelemetryRepository(session).create_many(rows)
            
        except Exception as e:
            logger.exception(f"Failed to persist telemetry batch: {e}")
            # Put back in buffer if it fails
            with self._lock:
                for reading in readings:
                    self._buffer.append(reading)
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    def record_execution(self, event, report, severity="high"):
        """Save execution to database synchronously."""
        # Run in a separate thread to not block
        Thread(target=self._record_execution_sync, args=(event, report, severity), daemon=True).start()

    def resolve_incident(self, incident_id, health_after=None):
        """Persist physical incident resolution independently of MAO completion.

        A successful investigation is evidence that the agents finished their
        work; it is not evidence that field conditions have normalized.
        """
        Thread(
            target=self._resolve_incident_sync,
            args=(incident_id, health_after),
            daemon=True,
        ).start()

    def _resolve_incident_sync(self, incident_id, health_after):
        session = None
        try:
            session = get_session()
            if session is None:
                return
            incident = session.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
            if incident is None:
                return
            resolved_at = datetime.utcnow()
            incident.status = "resolved"
            incident.resolved_at = resolved_at
            if health_after is not None:
                incident.health_after = float(health_after)
            if incident.created_at:
                incident.resolution_seconds = round(
                    max(0.0, (resolved_at - incident.created_at).total_seconds()), 2
                )
            session.commit()
        except Exception as error:
            if session:
                session.rollback()
            logger.exception("Failed to persist incident resolution: %s", error)
        finally:
            if session:
                session.close()
    
    def _record_execution_sync(self, event, report, severity):
        """Sync version for execution."""
        session = None
        try:
            session = get_session()
            if session is None:
                return
            
            # Create incident
            incident = IncidentDB(
                id=getattr(event, 'id', 'unknown'),
                asset_id=getattr(event, 'source', 'unknown'),
                event=getattr(event, 'name', 'unknown'),
                severity=severity,
                # This records the physical-operational lifecycle, not merely
                # the MAO workflow lifecycle. Resolution is recorded later by
                # the simulator after readings normalize.
                status="under_investigation" if getattr(report, 'success', False) else "requires_review",
                report=getattr(report, 'final_summary', ''),
                health_before=(getattr(event, "payload", {}) or {}).get("health_before"),
                health_after=None,
                resolution_seconds=None,
                resolved_at=None,
                created_at=getattr(event, 'timestamp', datetime.now()),
            )
            asset = None
            try:
                from services.runtime import runtime
                asset = runtime.kernel.asset_service.get(getattr(event, "source", ""))
            except Exception:
                pass
            incident.health_after = getattr(asset, "health", None)
            IncidentRepository(session).create(incident)

            # Create execution report
            stored_report = ExecutionReportDB(
                id=getattr(report, 'id', 'unknown'),
                execution_id=getattr(report, 'execution_id', 'unknown'),
                incident_id=getattr(event, 'id', 'unknown'),
                workflow=getattr(report, 'workflow_name', 'unknown'),
                success=getattr(report, 'success', False),
                summary=getattr(report, 'final_summary', ''),
                recommendations=getattr(report, 'recommendations', []),
                started_at=getattr(report, 'started_at', datetime.now()),
                completed_at=getattr(report, 'completed_at', datetime.now()),
            )
            ReportRepository(session).create(stored_report)

            # Create agent results
            agent_results = getattr(report, 'agent_results', [])
            if agent_results:
                agent_rows = [
                    AgentExecutionDB(
                        id=getattr(result, 'id', 'unknown'),
                        incident_id=getattr(event, 'id', 'unknown'),
                        agent_name=getattr(result, 'agent_name', 'unknown'),
                        task=result.metadata.get("task_name", "") if hasattr(result, 'metadata') else "",
                        input=result.metadata.get("task_description", "") if hasattr(result, 'metadata') else "",
                        output=getattr(result, 'summary', ''),
                        success=getattr(result, 'success', False),
                        confidence=getattr(result, 'confidence', 0.0),
                        summary=getattr(result, 'summary', ''),
                        recommendations=getattr(result, 'recommendations', []),
                        decision=getattr(result, 'decision', ''),
                        evidence=getattr(result, 'evidence', []),
                        actions_required=getattr(result, 'actions_required', []),
                        requires_human_approval=getattr(result, 'requires_human_approval', False),
                        timestamp=getattr(result, 'timestamp', datetime.now()),
                    )
                    for result in agent_results
                ]
                AgentRepository(session).create_many(agent_rows)
            
            session.commit()
            
        except Exception as e:
            if session:
                session.rollback()
            logger.exception(f"Failed to persist execution: {e}")
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    def shutdown(self):
        """Shutdown the service and flush remaining data."""
        self._running = False
        self._flush_buffer()


# ✅ Singleton instance
_persistence = None


def get_persistence():
    """Get the singleton persistence service."""
    global _persistence
    if _persistence is None:
        _persistence = PersistenceService()
    return _persistence
