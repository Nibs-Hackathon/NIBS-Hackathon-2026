"""Unified backend API for frontend access with lazy loading and caching."""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from functools import lru_cache
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel, simulator
from services.config_services import ConfigService


class BackendAPI:
    """Single interface for frontend to access backend data with caching."""

    def __init__(self):
        self.config = ConfigService()
        self._cache_ttl = 5  # seconds
        self._cache_timestamps = {}

    def _is_cache_valid(self, key: str) -> bool:
        """Check if cache entry is still valid."""
        if key not in self._cache_timestamps:
            return False
        return (time.time() - self._cache_timestamps[key]) < self._cache_ttl

    def _invalidate_cache(self, key: str = None):
        """Invalidate cache for a specific key or all keys."""
        if key:
            self._cache_timestamps.pop(key, None)
            # Also clear lru_cache for this method
            if hasattr(self, f"_{key}_cached"):
                getattr(self, f"_{key}_cached").cache_clear()
        else:
            self._cache_timestamps.clear()
            # Clear all lru_caches
            for attr in dir(self):
                if attr.startswith("_") and attr.endswith("_cached"):
                    getattr(self, attr).cache_clear()

    # -------------------------
    # Asset Operations (with Caching)
    # -------------------------

    @lru_cache(maxsize=32)
    def _get_assets_cached(self) -> List[Dict]:
        """Cached version of get_assets."""
        assets = kernel.asset_service.all_assets()
        return [
            {
                "id": asset.id,
                "name": asset.name,
                "type": asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type),
                "location": asset.location,
                "health": asset.health,
                "status": asset.status,
            }
            for asset in assets
        ]

    def get_assets(self, force_refresh: bool = False) -> List[Dict]:
        """Get all assets from the runtime with caching."""
        if force_refresh:
            self._invalidate_cache("get_assets")
        return self._get_assets_cached()

    @lru_cache(maxsize=128)
    def _get_asset_telemetry_cached(self, asset_id: str, limit: int = 100) -> tuple:
        """Cached version of get_asset_telemetry."""
        readings = kernel.state.get_history(asset_id)
        if limit:
            readings = readings[-limit:]
        return tuple([
            {
                "timestamp": r.timestamp.isoformat(),
                "sensor_type": r.sensor_type.value if hasattr(r.sensor_type, 'value') else str(r.sensor_type),
                "value": r.value,
                "unit": getattr(r, 'unit', ''),
            }
            for r in readings
        ])

    def get_asset_telemetry(self, asset_id: str, limit: int = 100, force_refresh: bool = False) -> List[Dict]:
        """Get telemetry history for an asset with caching."""
        if force_refresh:
            self._invalidate_cache("get_asset_telemetry")
        return list(self._get_asset_telemetry_cached(asset_id, limit))

    def get_asset_health(self, asset_id: str) -> Dict:
        """Get health for a specific asset."""
        readings = kernel.state.get_history(asset_id)
        health = kernel.health.calculate_health(readings)
        return {
            "health": health,
            "readings": len(readings),
            "status": "Running" if health > 80 else "Warning" if health > 50 else "Critical",
        }

    # -------------------------
    # Incident Operations (with Caching)
    # -------------------------

    @lru_cache(maxsize=32)
    def _get_incidents_cached(self) -> tuple:
        """Cached version of get_incidents."""
        events = kernel.event_store.all()
        return tuple([
            {
                "id": event.id,
                "name": event.name,
                "asset_id": event.source,
                "payload": event.payload,
                "timestamp": event.timestamp.isoformat(),
            }
            for event in events
        ])

    def get_incidents(self, force_refresh: bool = False) -> List[Dict]:
        """Get all incidents from the runtime with caching."""
        if force_refresh:
            self._invalidate_cache("get_incidents")
        return list(self._get_incidents_cached())

    def trigger_incident(self, incident_type: str) -> Dict:
        """Trigger a simulated incident."""
        from services.incident_service import IncidentService
        service = IncidentService(simulator)
        result = service.trigger_incident(incident_type)
        # Invalidate caches after new incident
        self._invalidate_cache("get_incidents")
        self._invalidate_cache("get_agent_activity")
        return result

    # -------------------------
    # Agent Operations (with Caching)
    # -------------------------

    @lru_cache(maxsize=32)
    def _get_agents_cached(self) -> List[Dict]:
        """Cached version of get_agents."""
        agents = kernel.registry.all()
        results = kernel.state.agent_results
        result_map = {r.agent_name: r for r in results}
        return [
            {
                "name": agent.name,
                "status": "Active" if agent.name in result_map else "Ready",
                "last_result": result_map.get(agent.name),
            }
            for agent in agents
        ]

    def get_agents(self, force_refresh: bool = False) -> List[Dict]:
        """Get registered agents and their status with caching."""
        if force_refresh:
            self._invalidate_cache("get_agents")
        return self._get_agents_cached()

    @lru_cache(maxsize=32)
    def _get_agent_activity_cached(self, limit: int = 50) -> tuple:
        """Cached version of get_agent_activity."""
        results = kernel.state.agent_results[-limit:]
        return tuple([
            {
                "agent_name": r.agent_name,
                "finding": r.finding,
                "confidence": r.confidence,
                "success": r.success,
                "timestamp": r.timestamp.isoformat(),
                "summary": r.summary,
                "recommendations": r.recommendations,
            }
            for r in results
        ])

    def get_agent_activity(self, limit: int = 50, force_refresh: bool = False) -> List[Dict]:
        """Get recent agent activity with caching."""
        if force_refresh:
            self._invalidate_cache("get_agent_activity")
        return list(self._get_agent_activity_cached(limit))

    # -------------------------
    # Report Operations (with Caching)
    # -------------------------

    @lru_cache(maxsize=32)
    def _get_reports_cached(self) -> tuple:
        """Cached version of get_reports."""
        reports = kernel.state.execution_reports
        return tuple([
            {
                "id": r.id,
                "workflow": r.workflow_name,
                "success": r.success,
                "summary": r.final_summary,
                "started_at": r.started_at.isoformat(),
                "completed_at": r.completed_at.isoformat(),
                "confidence": r.average_confidence,
                "agent_results": len(r.agent_results),
            }
            for r in reports
        ])

    def get_reports(self, force_refresh: bool = False) -> List[Dict]:
        """Get execution reports with caching."""
        if force_refresh:
            self._invalidate_cache("get_reports")
        return list(self._get_reports_cached())

    # -------------------------
    # Configuration
    # -------------------------

    def get_dynamic_thresholds(self, asset_type: str) -> Dict:
        """Get Gemini-generated thresholds for an asset type."""
        return self.config.get_thresholds(asset_type)

    def get_workflow_sequence(self, incident_type: str) -> List[str]:
        """Get Gemini-generated workflow sequence."""
        return self.config.get_workflow_sequence(incident_type)

    def refresh_config(self) -> Dict:
        """Refresh all configurations and clear caches."""
        self.config.refresh()
        self._invalidate_cache()  # Clear all caches
        return {"status": "refreshed", "cache_cleared": True}

    # -------------------------
    # Simulation Control
    # -------------------------

    def get_simulation_status(self) -> Dict:
        """Get current simulation status."""
        return {
            "running": getattr(kernel, "_simulation_running", False),
            "events": len(kernel.event_store.all()),
            "reports": len(kernel.state.execution_reports),
            "agent_results": len(kernel.state.agent_results),
            "assets": len(kernel.asset_service.all_assets()),
        }

    def step_simulation(self) -> Dict:
        """Advance simulation by one tick."""
        from services.simulator_controller import sim_controller
        telemetry, reports = sim_controller.step()
        # Invalidate caches after simulation step
        self._invalidate_cache()
        return {
            "telemetry_count": len(telemetry),
            "reports_count": len(reports),
        }


# Singleton instance
api = BackendAPI()