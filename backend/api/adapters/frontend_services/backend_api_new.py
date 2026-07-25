"""Unified backend API for frontend access with caching and refinery support."""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from functools import lru_cache
import time
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.config_services import ConfigService


class BackendAPI:
    """Single interface for frontend to access backend data with caching."""

    def __init__(self):
        self.config = ConfigService()
        self._cache_ttl = 5
        self._cache_timestamps = {}
        self._kernel = None
        self._simulator = None

    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_timestamps:
            return False
        return (time.time() - self._cache_timestamps[key]) < self._cache_ttl

    def _invalidate_cache(self, key: str = None):
        if key:
            self._cache_timestamps.pop(key, None)
            if hasattr(self, f"_{key}_cached"):
                getattr(self, f"_{key}_cached").cache_clear()
        else:
            self._cache_timestamps.clear()
            for attr in dir(self):
                if attr.startswith("_") and attr.endswith("_cached"):
                    getattr(self, attr).cache_clear()

    def _get_runtime(self):
        """Lazy load runtime to avoid circular imports."""
        if self._kernel is None or self._simulator is None:
            from services.runtime import runtime
            self._kernel = runtime.kernel
            self._simulator = runtime.simulator
        return self._kernel, self._simulator

    @property
    def kernel(self):
        return self._get_runtime()[0]

    @property
    def simulator(self):
        return self._get_runtime()[1]

    def get_refineries(self) -> List[Dict]:
        """Get all refineries with their assets."""
        refineries = getattr(self.kernel, "_refineries", [])
        return [
            {
                "id": r.id,
                "name": r.name,
                "location": r.location,
                "status": r.status,
                "asset_count": len(r.assets),
                "assets": [
                    {
                        "id": a.id,
                        "name": a.name,
                        "type": a.asset_type.value if hasattr(a.asset_type, 'value') else str(a.asset_type),
                        "health": a.health,
                        "status": a.status,
                        "zone": getattr(a, "zone", "Unassigned"),
                    }
                    for a in r.assets
                ]
            }
            for r in refineries
        ]

    def get_refinery_assets(self, refinery_id: str) -> List[Dict]:
        """Get assets for a specific refinery."""
        refineries = getattr(self.kernel, "_refineries", [])
        for refinery in refineries:
            if refinery.id == refinery_id:
                return [
                    {
                        "id": a.id,
                        "name": a.name,
                        "type": a.asset_type.value if hasattr(a.asset_type, 'value') else str(a.asset_type),
                        "health": a.health,
                        "status": a.status,
                        "zone": getattr(a, "zone", "Unassigned"),
                        "refinery_id": refinery.id,
                        "refinery_name": refinery.name,
                    }
                    for a in refinery.assets
                ]
        return []

    def get_assets_by_type(self, refinery_id: str, asset_type: str) -> List[Dict]:
        """Get assets of a specific type in a refinery."""
        all_assets = self.get_refinery_assets(refinery_id)
        return [a for a in all_assets if a.get("type", "").lower() == asset_type.lower()]

    @lru_cache(maxsize=32)
    def _get_assets_cached(self) -> List[Dict]:
        """Cached version of get_assets."""
        assets = self.kernel.asset_service.all_assets()
        return [
            {
                "id": asset.id,
                "name": asset.name,
                "type": asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type),
                "location": asset.location,
                "zone": getattr(asset, "zone", "Unassigned"),
                "health": asset.health,
                "status": asset.status,
                "refinery_id": getattr(asset, "refinery_id", None),
            }
            for asset in assets
        ]

    def get_assets(self, force_refresh: bool = False) -> List[Dict]:
        """Get all assets from all refineries with caching."""
        if force_refresh:
            self._invalidate_cache("get_assets")
        return self._get_assets_cached()

    @lru_cache(maxsize=128)
    @lru_cache(maxsize=128)
    def _get_asset_telemetry_cached(self, asset_id: str, limit: int = 100) -> tuple:
        """Cached version of get_asset_telemetry."""
        readings = self.kernel.state.get_history(asset_id)
        if limit:
            readings = readings[-limit:]
        return tuple([
            {
                "timestamp": r.timestamp.isoformat() if hasattr(r, 'timestamp') else datetime.now().isoformat(),
                "sensor_type": r.sensor_type.value if hasattr(r.sensor_type, 'value') else str(r.sensor_type),
                "value": float(r.value) if hasattr(r, 'value') else 0,
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
        readings = self.kernel.state.get_history(asset_id)
        health = self.kernel.health.calculate_health(readings)
        return {
            "health": health,
            "readings": len(readings),
            "status": "Running" if health > 80 else "Warning" if health > 50 else "Critical",
        }

    @lru_cache(maxsize=32)
    def _get_incidents_cached(self) -> tuple:
        """Cached version of get_incidents."""
        events = self.kernel.event_store.all()
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
        service = IncidentService(self.simulator)
        result = service.trigger_incident(incident_type)
        self._invalidate_cache("get_incidents")
        self._invalidate_cache("get_agent_activity")
        return result

    @lru_cache(maxsize=32)
    def _get_agents_cached(self) -> List[Dict]:
        """Cached version of get_agents."""
        agents = self.kernel.registry.all()
        results = self.kernel.state.agent_results
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
        results = self.kernel.state.agent_results[-limit:]
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

    @lru_cache(maxsize=32)
    def _get_reports_cached(self) -> tuple:
        """Cached version of get_reports."""
        reports = self.kernel.state.execution_reports
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

    def get_dynamic_thresholds(self, asset_type: str) -> Dict:
        """Get Gemini-generated thresholds for an asset type."""
        return self.config.get_thresholds(asset_type)

    def get_workflow_sequence(self, incident_type: str) -> List[str]:
        """Get Gemini-generated workflow sequence."""
        return self.config.get_workflow_sequence(incident_type)

    def refresh_config(self) -> Dict:
        """Refresh all configurations and clear caches."""
        self.config.refresh()
        self._invalidate_cache()
        return {"status": "refreshed", "cache_cleared": True}

    def get_simulation_status(self) -> Dict:
        """Get current simulation status."""
        return {
            "running": getattr(self.kernel, "_simulation_running", False),
            "events": len(self.kernel.event_store.all()),
            "reports": len(self.kernel.state.execution_reports),
            "agent_results": len(self.kernel.state.agent_results),
            "assets": len(self.kernel.asset_service.all_assets()),
        }

    def step_simulation(self) -> Dict:
        """Advance simulation by one tick."""
        from services.simulator_controller import sim_controller
        telemetry, reports = sim_controller.step()
        self._invalidate_cache()
        return {
            "telemetry_count": len(telemetry),
            "reports_count": len(reports),
        }


# ✅ Create the singleton instance
_api_instance = None


def _get_api_instance():
    global _api_instance
    if _api_instance is None:
        _api_instance = BackendAPI()
    return _api_instance


# ✅ Export api as a property that lazy-loads
class _ApiProxy:
    def __getattr__(self, name):
        return getattr(_get_api_instance(), name)


api = _ApiProxy()
BackendAPI = BackendAPI