"""Optimized persistence service with async/batch operations."""

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Any

from database.connection import get_session
from database.models import AgentExecutionDB, ExecutionReportDB, IncidentDB, TelemetryDB
from database.repositories.agent_repo import AgentRepository
from database.repositories.incident_repo import IncidentRepository
from database.repositories.report_repo import ReportRepository
from database.repositories.telemetry_repo import TelemetryRepository
import time
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

    def _record_telemetry_sync(self, readings):
        """Sync version for background thread - with retry logic."""
        if not readings:
            return
        
        max_retries = 3
        for attempt in range(max_retries):
            session = get_session()
            try:
                # ✅ Process in smaller batches
                batch_size = 50
                for i in range(0, len(readings), batch_size):
                    batch = readings[i:i + batch_size]
                    rows = [
                        TelemetryDB(
                            asset_id=reading.asset_id,
                            sensor_type=reading.sensor_type.value,
                            value=reading.value,
                            timestamp=reading.timestamp,
                        )
                        for reading in batch
                    ]
                    TelemetryRepository(session).create_many(rows)
                break  # Success - exit retry loop
            except Exception as e:
                session.rollback()
                logger.warning(f"Telemetry save attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    logger.exception("Failed to persist telemetry after retries.")
                time.sleep(1)  # Wait before retry
            finally:
                session.close()

    def wait_for_persistence(self):
        """Wait for all pending persistence operations to complete."""
        _pool.shutdown(wait=True)