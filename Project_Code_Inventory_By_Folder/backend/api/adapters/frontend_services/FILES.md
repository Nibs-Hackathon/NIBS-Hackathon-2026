# Folder: backend/api/adapters/frontend_services Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/api/adapters/frontend_services`

Contains 16 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/api/adapters/frontend_services/__init__.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/__init__.py`

```python
"""Frontend-facing adapters for existing RigOS backend modules."""

from app.frontend_services.backend_api_new import api, BackendAPI

# Import all adapters directly
from app.frontend_services.dashboard_adapter import get_dashboard
from app.frontend_services.asset_adapter import get_assets
from app.frontend_services.agent_adapter import get_agents, get_agent_metrics
from app.frontend_services.report_adapter import get_reports
from app.frontend_services.control_adapter import get_control_state
from app.frontend_services.telemetry_adapter import get_asset_telemetry
from app.frontend_services.health_adapter import get_asset_health
from app.frontend_services.health_prediction_adapter import get_health_prediction
from app.frontend_services.knowledge_adapter import KnowledgeSearchError, search_knowledge
from app.frontend_services.knowledge_agent_adapter import KnowledgeAgentUnavailable, ask_knowledge_agent, is_operational_query
from app.frontend_services.incident_adapter import trigger_incident, get_incidents
from app.frontend_services.maintenance_adapter import get_maintenance_plan
from app.frontend_services.digital_twin_adapter import get_twin_assets
from app.frontend_services.agent_activity_adapter import get_agent_activity

__all__ = [
    "api",
    "BackendAPI",
    "get_dashboard",
    "get_assets",
    "get_agents",
    "get_agent_metrics",
    "get_reports",
    "get_control_state",
    "get_asset_telemetry",
    "get_asset_health",
    "get_health_prediction",
    "KnowledgeSearchError",
    "search_knowledge",
    "KnowledgeAgentUnavailable",
    "ask_knowledge_agent",
    "is_operational_query",
    "trigger_incident",
    "get_incidents",
    "get_maintenance_plan",
    "get_twin_assets",
    "get_agent_activity",
]
```

## backend/api/adapters/frontend_services/agent_activity_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/agent_activity_adapter.py`

```python
"""Activity view-model sourced from live MAO state and persisted audit events."""

from datetime import datetime
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import get_session
from database.repositories.activity_repo import ActivityRepository
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _format_time(timestamp) -> str:
    return timestamp.strftime("%H:%M:%S") if timestamp else "Unknown"


def _runtime_activity() -> list[dict]:
    kernel = runtime.kernel
    return [
        {
            "time": _format_time(getattr(result, "timestamp", None)),
            "agent": result.agent_name,
            "action": result.summary or result.finding or "No summary recorded.",
            "state": "Completed" if result.success else "Failed",
            "confidence": f"{round(result.confidence * 100)}%",
            "progress": 100,
            "timestamp": getattr(result, "timestamp", None),
        }
        for result in kernel.state.agent_results
    ]


def _persisted_activity() -> tuple[list[dict], str | None]:
    """Load immutable activity records without blocking live state rendering."""
    session = None
    try:
        session = get_session()
        events = ActivityRepository(session).get_recent()
        return [
            {
                "time": _format_time(event.created_at),
                "agent": event.source,
                "action": event.summary,
                "state": event.status.title(),
                "confidence": (
                    f"{round(event.confidence * 100)}%"
                    if event.confidence is not None
                    else "Not available"
                ),
                "progress": 100 if event.status.lower() == "completed" else 0,
                "timestamp": event.created_at,
            }
            for event in events
        ], None
    except Exception:
        return [], "Persisted activity is temporarily unavailable."
    finally:
        if session is not None:
            session.close()


def get_agent_activity() -> tuple[list[dict], str | None]:
    """Return the combined live MAO and persisted activity timeline."""
    runtime_events = _runtime_activity()
    persisted_events, warning = _persisted_activity()
    activity = runtime_events + persisted_events
    activity.sort(key=lambda event: event["timestamp"] or datetime.min, reverse=True)
    return activity, warning


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return summary metrics from current MAO agent results."""
    kernel = runtime.kernel
    results = kernel.state.agent_results

    if not results:
        return [
            ("Activities today", "0", "Waiting for execution", "cyan"),
            ("Completed workflows", "0", "No executions", "green"),
            ("Human reviews", "0", "No pending review", "amber"),
            ("Avg confidence", "0%", "No data", "violet"),
        ]

    completed = sum(result.success for result in results)
    confidence = sum(result.confidence for result in results) / len(results)
    reviews = sum(result.requires_human_approval for result in results)

    return [
        ("Activities today", str(len(results)), "From MAO execution", "cyan"),
        ("Completed workflows", str(completed), "Successful executions", "green"),
        ("Human reviews", str(reviews), "Approval required", "amber"),
        ("Avg confidence", f"{round(confidence * 100, 1)}%", "Agent confidence", "violet"),
    ]
```

## backend/api/adapters/frontend_services/agent_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/agent_adapter.py`

```python
"""Agent adapter using BackendAPI."""

from __future__ import annotations

from app.frontend_services.backend_api_new import api


def get_agents() -> list[dict[str, str]]:
    """Return registered agents and their latest execution state."""
    agents_data = api.get_agents()
    activity = api.get_agent_activity(limit=20)
    
    # Map agent names to latest results
    latest_results = {}
    for a in activity:
        if a["agent_name"] not in latest_results:
            latest_results[a["agent_name"]] = a
    
    agents = []
    for agent in agents_data:
        name = agent["name"]
        result = latest_results.get(name)
        agents.append({
            "Agent": name.replace("_", " ").title(),
            "Specialty": name.title(),
            "State": "Active" if result and result.get("success") else "Ready",
            "Confidence": f"{round(result.get('confidence', 0) * 100)}%" if result else "N/A",
            "Current task": result.get("finding", "Awaiting task")[:50] if result else "Awaiting task",
        })
    return agents


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return monitor metrics calculated from the live state."""
    agents_data = api.get_agents()
    activity = api.get_agent_activity(limit=50)
    status = api.get_simulation_status()
    
    registered = len(agents_data)
    results = len(activity)
    success_count = sum(1 for a in activity if a.get("success"))
    avg_confidence = sum(a.get("confidence", 0) for a in activity) / len(activity) if activity else 0
    
    return [
        ("Agents registered", str(registered), "Shared MAO registry", "green"),
        ("Tasks active", str(status.get("reports", 0)), "Execution reports", "amber"),
        ("Avg. confidence", f"{round(avg_confidence * 100, 1)}%" if avg_confidence else "N/A", "From completed agent results", "cyan"),
        ("Decisions recorded", str(results), "MAO agent executions", "violet"),
    ]
```

## backend/api/adapters/frontend_services/asset_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/asset_adapter.py`

```python
"""Asset adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api


def get_assets():
    """Get all assets with telemetry history."""
    assets = api.get_assets()
    
    # Get telemetry for each asset
    for asset in assets:
        telemetry = api.get_asset_telemetry(asset["id"], limit=1)
        if telemetry:
            asset["Last telemetry"] = telemetry[-1].get("timestamp", "N/A")[:19] if "timestamp" in telemetry[-1] else "N/A"
        else:
            asset["Last telemetry"] = "No data"
    
    return {
        "assets": assets,
        "sensors": [
            {"Sensor": "Pressure", "Reading": "119.4 bar", "State": "Normal"},
            {"Sensor": "Temperature", "Reading": "76.2 °C", "State": "Normal"},
            {"Sensor": "Vibration", "Reading": "23.7 mm/s", "State": "Watch"},
            {"Sensor": "Flow", "Reading": "63.1 m³/h", "State": "Normal"},
        ],
        "history": []
    }
```

## backend/api/adapters/frontend_services/backend_api_new.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/backend_api_new.py`

```python
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
```

## backend/api/adapters/frontend_services/control_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/control_adapter.py`

```python
"""Control adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api


def get_control_state() -> dict:
    """Return a facility snapshot derived from live state."""
    assets = api.get_assets()
    incidents = api.get_incidents()
    status = api.get_simulation_status()
    
    if not assets:
        return {
            "facility_mode": "NO ASSETS",
            "throughput": "N/A",
            "safety": "0 / 0",
            "queue": "0",
            "zones": [],
            "summary": "No assets are registered with the shared MAO runtime.",
        }
    
    healthy_assets = [a for a in assets if a.get("status", "").lower() in {"running", "healthy"}]
    average_health = sum(a.get("health", 0) for a in assets) / len(assets) if assets else 0
    facility_mode = "RUNNING" if healthy_assets else "ATTENTION"
    
    # Group by zone
    zones: dict[str, dict] = {}
    for asset in assets:
        zone = asset.get("location", "Unassigned")
        zones.setdefault(zone, {"assets": 0, "health": []})
        zones[zone]["assets"] += 1
        zones[zone]["health"].append(asset.get("health", 0))
    
    zone_snapshot = []
    for name, data in sorted(zones.items()):
        average_zone_health = sum(data["health"]) / len(data["health"]) if data["health"] else 0
        zone_snapshot.append({
            "Zone": name,
            "State": "Nominal" if average_zone_health >= 80 else "Attention",
            "Health": f"{round(average_zone_health)}%",
            "Assets": data["assets"],
        })
    
    return {
        "facility_mode": facility_mode,
        "throughput": f"{round((len(healthy_assets) / len(assets)) * 100, 1)}%" if assets else "N/A",
        "safety": f"{len(healthy_assets)} / {len(assets)}",
        "queue": str(len(incidents)),
        "zones": zone_snapshot,
        "summary": f"{len(healthy_assets)} of {len(assets)} registered assets are operating normally; average asset health is {round(average_health, 1)}%.",
    }
```

## backend/api/adapters/frontend_services/dashboard_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/dashboard_adapter.py`

```python
"""Dashboard adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def calculate_severity(event):
    """Calculate severity from event payload."""
    payload = event.get("payload", {})

    if "gas" in payload:
        return "Critical"
    if "pressure" in payload:
        return "Critical" if payload["pressure"] > 160 else "High"
    if "temperature" in payload:
        return "Critical" if payload["temperature"] > 100 else "High"
    if "vibration" in payload:
        return "Critical" if payload["vibration"] > 40 else "High"
    if "flow" in payload:
        return "Medium"
    return "Unknown"


def get_dashboard():
    """Get dashboard data using BackendAPI with caching."""
    # Get data from API (uses caching internally)
    assets = api.get_assets()
    incidents = api.get_incidents()
    activity = api.get_agent_activity(limit=5)

    # ✅ Use runtime.kernel
    kernel = runtime.kernel

    # Calculate metrics
    total_assets = len(assets)
    healthy_assets = sum(1 for a in assets if a.get("status") == "Running")
    avg_health = sum(a.get("health", 0) for a in assets) / total_assets if total_assets else 0

    metrics = [
        ("Fleet health", f"{avg_health:.1f}%", "Calculated from assets", "green"),
        ("Assets online", f"{healthy_assets} / {total_assets}", "Connected", "cyan"),
        ("Active incidents", str(len(incidents)), "From EventStore", "red"),
        ("AI decisions", str(len(kernel.state.agent_results)), "Agent executions", "violet"),
    ]

    # Format incidents
    formatted_incidents = []
    for incident in incidents[-10:]:
        formatted_incidents.append({
            "Incident": incident.get("name", "Unknown"),
            "Asset": incident.get("asset_id", "Unknown"),
            "Severity": calculate_severity(incident),
            "Detected": incident.get("timestamp", "").split("T")[1][:8] if "T" in incident.get("timestamp", "") else "",
        })

    # Format activity
    formatted_activity = []
    for a in activity[:5]:
        timestamp = a.get("timestamp", "")
        time_str = timestamp.split("T")[1][:8] if "T" in timestamp else ""
        formatted_activity.append((
            time_str,
            a.get("agent_name", "Unknown"),
            a.get("summary", "")[:100],
        ))

    return {
        "metrics": metrics,
        "incidents": formatted_incidents,
        "assets": assets,
        "activity": formatted_activity,
    }
```

## backend/api/adapters/frontend_services/digital_twin_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/digital_twin_adapter.py`

```python
"""Read-only asset and telemetry view-model for the Digital Twin page."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _reading_value(readings: list[Any], sensor_type: str) -> str:
    for reading in reversed(readings):
        reading_type = getattr(reading.sensor_type, "value", reading.sensor_type)
        if str(reading_type).lower() == sensor_type.lower():
            value = getattr(reading, "value", "N/A")
            unit = getattr(reading, "unit", "")
            return f"{value} {unit}".strip()
    return "Not available"


def _maintenance_recommendation(asset_id: str) -> str:
    kernel = runtime.kernel
    for result in reversed(kernel.state.agent_results):
        if result.agent_name != "maintenance":
            continue
        if result.metadata.get("asset_id") != asset_id:
            continue
        recommendations = result.recommendations or result.evidence
        if recommendations:
            return recommendations[0]
    return "No maintenance recommendation is available for this asset."


def get_twin_assets() -> list[dict]:
    """Return current assets and latest observed telemetry from the runtime."""
    kernel = runtime.kernel
    assets = []
    for asset in kernel.asset_service.all_assets():
        readings = kernel.state.get_history(asset.id)
        health = kernel.health.calculate_health(readings) if readings else asset.health
        
        # ✅ Get actual telemetry values
        temp = _reading_value(readings, "temperature")
        pressure = _reading_value(readings, "pressure")
        rpm = _reading_value(readings, "rpm")
        
        assets.append({
            "id": asset.id,
            "Asset": asset.name,
            "Category": getattr(asset.asset_type, "value", str(asset.asset_type)),
            "Zone": asset.location or "Unassigned",
            "Status": asset.status or ("Healthy" if health >= 80 else "Attention"),
            "Health": round(health, 1),
            "Temperature": temp,
            "Pressure": pressure,
            "RPM": rpm,
            "Failure": "Not available",
            "Recommendation": _maintenance_recommendation(asset.id),
        })
    return assets
```

## backend/api/adapters/frontend_services/health_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/health_adapter.py`

```python
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def get_asset_health(asset_id):
    kernel = runtime.kernel
    readings = kernel.state.get_history(asset_id)

    health = kernel.health.calculate_health(
        readings
    )

    return {
        "health": health,
        "readings": readings
    }
```

## backend/api/adapters/frontend_services/health_prediction_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/health_prediction_adapter.py`

```python
"""Health prediction using computation engine."""

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime
from services.computation_engine import ComputationEngine


def get_health_prediction(asset_id, horizon_days=14):
    """Get health prediction using the computation engine."""
    kernel = runtime.kernel
    engine = ComputationEngine()
    
    readings = kernel.state.get_history(asset_id)
    asset = kernel.asset_service.get(asset_id)
    
    if not asset or not readings:
        return {
            "health": 100,
            "rul": "365 days",
            "failure_probability": "0%",
            "confidence": "Low",
            "historical": {"Historical health": []},
            "predicted": {"Predicted health": [], "Intervention threshold": []},
            "telemetry": []
        }
    
    # Get current metrics
    metrics = engine.compute_asset(asset, readings)
    
    # Calculate historical health
    historical = []
    for i in range(len(readings)):
        h = engine._calculate_health(
            readings[:i+1],
            engine.config.get_thresholds(metrics["asset_type"]),
            {}  # weights
        )
        historical.append(round(h, 1))
    
    # Predict future health
    current_health = metrics["health"]
    degradation_rate = metrics["degradation_rate"]
    
    predicted = []
    for day in range(horizon_days):
        health = current_health - (degradation_rate * 5 * (day + 1))
        predicted.append(round(max(0, health), 1))
    
    # Format RUL
    rul_days = metrics["rul_days"]
    if rul_days >= 365:
        rul_str = "365+ days"
    elif rul_days >= 90:
        rul_str = f"{int(rul_days)} days"
    elif rul_days >= 30:
        rul_str = f"{int(rul_days)} days"
    elif rul_days >= 7:
        rul_str = f"{int(rul_days)} days"
    else:
        rul_str = f"{int(rul_days)} days"
    
    return {
        "health": round(metrics["health"]),
        "rul": rul_str,
        "failure_probability": f"{metrics['failure_probability']:.1f}%",
        "confidence": f"{metrics['confidence'] * 100:.1f}%",
        "historical": {"Historical health": historical},
        "predicted": {
            "Predicted health": predicted,
            "Intervention threshold": [70] * horizon_days
        },
        "telemetry": format_telemetry(readings)
    }


def format_telemetry(readings):
    """Format telemetry for display."""
    data = []
    for reading in readings[-10:]:
        data.append({
            "Sensor": reading.sensor_type.value,
            "Observed": reading.value,
            "Time": reading.timestamp.strftime("%H:%M:%S")
        })
    return data
```

## backend/api/adapters/frontend_services/incident_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/incident_adapter.py`

```python
"""Incident adapter with dynamic severity calculation from config."""

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime
from services.incident_service import IncidentService
from services.ai_config import AIConfigGenerator


def trigger_incident(incident_type):
    """Trigger an incident and return formatted results."""
    simulator = runtime.simulator
    service = IncidentService(simulator)
    result = service.trigger_incident(incident_type)
    
    try:
        import streamlit as st
        reports = result.get("reports", [])
        if reports:
            events = []
            for i, report in enumerate(reports):
                agent_name = getattr(report, 'workflow_name', 'Unknown')
                if i == 0:
                    events.append(("⏱️ 00:00", "🚨 Incident detected"))
                events.append((f"⏱️ 00:{i+2:02d}", f"🤖 {agent_name} completed"))
            
            last_report = reports[-1] if reports else None
            if last_report:
                summary = getattr(last_report, 'final_summary', '')
                if "planning" in summary.lower():
                    events.append(("⏱️ 00:12", "✅ Investigation complete"))
            
            st.session_state.incident_events = events
            st.session_state.investigation_complete = True
    except Exception as e:
        print(f"⚠️ Could not update session state: {e}")
    
    return result


def get_incidents():
    """Get all incidents from the runtime."""
    kernel = runtime.kernel
    events = kernel.event_store.all()

    incidents = []
    for event in events:
        severity = calculate_severity(event)
        incidents.append({
            "Incident": event.name,
            "Asset": event.source,
            "Severity": severity,
            "Detected": event.timestamp.strftime("%H:%M:%S") if hasattr(event, 'timestamp') else "Unknown",
            "Payload": event.payload,
        })

    return incidents


def calculate_severity(event):
    """
    Calculate severity from event payload using dynamic thresholds from AI config.
    """
    payload = getattr(event, 'payload', {})
    
    try:
        config = AIConfigGenerator()
        asset_type = payload.get("asset_type", "Pump")
        thresholds = config.get_thresholds(asset_type)
        severity_map = config.get_config().get("severity_mapping", {
            "Critical": 1, "High": 2, "Medium": 3, "Low": 4
        })
        
        severity_scores = {}
        
        if "pressure" in payload:
            pressure_max = thresholds.get("pressure_max", 150)
            pressure_val = payload["pressure"]
            ratio = pressure_val / pressure_max
            if ratio >= 1.5:
                severity_scores["pressure"] = 1
            elif ratio >= 1.2:
                severity_scores["pressure"] = 2
            elif ratio >= 1.05:
                severity_scores["pressure"] = 3
            else:
                severity_scores["pressure"] = 4
        
        if "temperature" in payload:
            temp_max = thresholds.get("temperature_max", 85)
            temp_val = payload["temperature"]
            ratio = temp_val / temp_max
            if ratio >= 1.5:
                severity_scores["temperature"] = 1
            elif ratio >= 1.2:
                severity_scores["temperature"] = 2
            elif ratio >= 1.05:
                severity_scores["temperature"] = 3
            else:
                severity_scores["temperature"] = 4
        
        if "gas" in payload:
            gas_max = thresholds.get("gas_max", 40)
            gas_val = payload["gas"]
            ratio = gas_val / gas_max
            if ratio >= 1.5:
                severity_scores["gas"] = 1
            elif ratio >= 1.2:
                severity_scores["gas"] = 2
            elif ratio >= 1.05:
                severity_scores["gas"] = 3
            else:
                severity_scores["gas"] = 4
        
        if "vibration" in payload:
            vib_max = thresholds.get("vibration_max", 8)
            vib_val = payload["vibration"]
            ratio = vib_val / vib_max
            if ratio >= 1.5:
                severity_scores["vibration"] = 1
            elif ratio >= 1.2:
                severity_scores["vibration"] = 2
            elif ratio >= 1.05:
                severity_scores["vibration"] = 3
            else:
                severity_scores["vibration"] = 4
        
        if "flow" in payload:
            flow_min = thresholds.get("flow_min", 25)
            flow_val = payload["flow"]
            ratio = flow_min / flow_val if flow_val > 0 else 10
            if ratio >= 2:
                severity_scores["flow"] = 1
            elif ratio >= 1.5:
                severity_scores["flow"] = 2
            elif ratio >= 1.2:
                severity_scores["flow"] = 3
            else:
                severity_scores["flow"] = 4
        
        if severity_scores:
            worst_score = min(severity_scores.values())
            reverse_map = {v: k for k, v in severity_map.items()}
            return reverse_map.get(worst_score, "Medium")
        
    except Exception as e:
        print(f"⚠️ Severity calculation failed: {e}")
    
    return "Medium"
```

## backend/api/adapters/frontend_services/knowledge_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/knowledge_adapter.py`

```python
"""Read-only Knowledge Base access through the shared MAO kernel."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


class KnowledgeSearchError(RuntimeError):
    """Raised when the registered knowledge retrieval path is unavailable."""


__all__ = ["KnowledgeSearchError", "search_knowledge"]

def search_knowledge(query: str) -> list[dict[str, str]]:
    """Return normalized Neon retrieval results from the registered KnowledgeAgent."""
    normalized_query = query.strip()
    if not normalized_query:
        return []

    try:
        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise KnowledgeSearchError("Knowledge Agent is not available. Please ensure the knowledge base is loaded.")
        if agent.retriever is None:
            raise KnowledgeSearchError("Knowledge retriever is not initialized. Please build the knowledge base first.")
    except KnowledgeSearchError:
        raise
    except Exception as error:
        raise KnowledgeSearchError(f"Knowledge service unavailable: {str(error)[:100]}") from error

    try:
        documents = agent.retriever.retrieve(normalized_query)
    except Exception as error:
        raise KnowledgeSearchError(f"Retrieval failed: {str(error)[:100]}") from error

    results = []
    for document in documents:
        metadata = document.metadata or {}
        source = str(metadata.get("source", "Unknown source"))
        results.append(
            {
                "content": document.page_content,
                "source": source,
                "filename": Path(source).name or source,
            }
        )
    return results
```

## backend/api/adapters/frontend_services/knowledge_agent_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/knowledge_agent_adapter.py`

```python
"""Frontend routing for Command Nexus conversational and operational requests."""

from __future__ import annotations

from functools import lru_cache
import logging
from pathlib import Path
import re
import sys
from typing import TYPE_CHECKING, Callable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if TYPE_CHECKING:
    from agents.knowledge import KnowledgeAgent

LOGGER = logging.getLogger(__name__)
ProgressCallback = Callable[[str], None]

OPERATIONAL_KEYWORDS = (
    "asset", "compressor", "pump", "pipeline", "tank", "valve", "maintenance",
    "inspection", "incident", "alarm", "safety", "hazard", "pressure",
    "temperature", "vibration", "flow", "gas", "refinery", "sop", "procedure",
    "equipment", "motor", "turbine", "boiler", "heat exchanger", "reactor",
    "distillation", "column", "flare", "corrosion", "shutdown", "startup",
    "trip", "failure", "process", "telemetry", "sensor", "knowledge",
)


def is_operational_query(question: str) -> bool:
    """Return whether a question requires the refinery operations path."""
    normalized = re.sub(r"\s+", " ", question.strip().casefold())
    return bool(normalized and any(keyword in normalized for keyword in OPERATIONAL_KEYWORDS))


def generate_conversational_response(question: str) -> str:
    """Use Gemini for casual conversation without starting the operational path."""
    from services.llm import LLMManager

    prompt = f"""
You are Command Nexus, a polished industrial operations copilot.

Reply naturally to this casual user message: {question!r}

Keep the response concise, warm, and professional. You may introduce yourself
as an industrial operations copilot and offer help with refinery operations,
equipment, maintenance, incident response, and safety. Do not provide
operational facts, citations, or technical instructions for a casual message.
Never mention implementation, search, retrieval, documents, a knowledge base,
databases, RAG, prompts, APIs, or model internals.
"""
    try:
        return LLMManager().generate(prompt)
    except Exception as e:
        LOGGER.error(f"Conversational response failed: {e}")
        return "I'm here to help with refinery operations. What would you like to know?"


def _emit(callback: ProgressCallback | None, message: str) -> None:
    LOGGER.info(message)
    if callback is not None:
        callback(message)


class KnowledgeAgentUnavailable(RuntimeError):
    """Raised when the existing backend knowledge path cannot serve a query."""


@lru_cache(maxsize=1)
def get_knowledge_agent() -> "KnowledgeAgent":
    """Return the KnowledgeAgent registered on the shared MAO kernel."""
    try:
        from services.runtime import runtime
        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise RuntimeError("KnowledgeAgent is not registered on the MAO kernel.")
        return agent
    except Exception as error:
        raise KnowledgeAgentUnavailable("Command Nexus is temporarily unavailable. Please try again shortly.") from error


def ask_knowledge_agent(question: str, on_progress: ProgressCallback | None = None) -> str:
    """Route casual conversation to Gemini and operational questions to KnowledgeAgent."""
    _emit(on_progress, "Command Nexus received a question.")
    normalized_question = question.strip()
    if not normalized_question:
        raise KnowledgeAgentUnavailable("Enter a question before asking Command Nexus.")

    if not is_operational_query(normalized_question):
        _emit(on_progress, "Conversational request detected.")
        try:
            return generate_conversational_response(normalized_question)
        except Exception as error:
            LOGGER.exception("Command Nexus conversational response failed")
            return "I'm here to help! What would you like to know about refinery operations?"

    _emit(on_progress, "Preparing an operational assessment.")
    try:
        from mao.models.task import Task

        task = Task(
            name="Operator knowledge query",
            description=normalized_question,
            assigned_agent="knowledge",
        )
        agent = get_knowledge_agent()
        
        if agent.retriever is None:
            return "The knowledge base is not available. Please ensure the database is configured and has documents loaded."

        result = agent.execute(task)
        
        if not result.success or not result.summary:
            return "I couldn't find specific operational guidance for that query. Please check with your operations team."
            
        return result.summary
        
    except Exception as error:
        LOGGER.exception("Command Nexus operational response failed")
        return "I'm having trouble accessing the knowledge base right now. Please try again later."
```

## backend/api/adapters/frontend_services/maintenance_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/maintenance_adapter.py`

```python
"""Read-only maintenance planning data from the shared MAO runtime."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


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


def get_maintenance_plan() -> dict:
    """Format state-manager tasks and agent output for the planner UI."""
    kernel = runtime.kernel
    results = _result_index()
    rows = []
    for task in kernel.state.get_tasks():
        result = results.get((task.name, task.assigned_agent))
        rows.append(
            {
                "Priority": _priority_label(task.priority),
                "Asset": _task_asset_name(task, result),
                "Work order": task.description,
                "Owner": task.assigned_agent.replace("_", " ").title(),
                "State": "Completed" if result and result.success else task.status.value.title(),
                "Confidence": (
                    f"{round(result.confidence * 100)}%" if result else "Not available"
                ),
            }
        )

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
```

## backend/api/adapters/frontend_services/report_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/report_adapter.py`

```python
"""Report adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api


def get_reports():
    """Get execution reports."""
    reports_data = api.get_reports()
    
    formatted_reports = []
    for report in reports_data[-10:]:
        formatted_reports.append({
            "Report": report["id"][:8],
            "Title": report["workflow"],
            "Workflow": report["workflow"],
            "Status": "Completed" if report["success"] else "Escalated",
            "Generated": report["completed_at"][:16] if "completed_at" in report else "N/A",
        })
    
    preview = {}
    if reports_data:
        latest = reports_data[-1]
        preview = {
            "Report": latest["id"][:8],
            "Title": latest["workflow"],
            "Summary": latest["summary"][:200] + "..." if len(latest.get("summary", "")) > 200 else latest.get("summary", ""),
            "Recommendation": "Review execution report for details."
        }
    
    metrics = [
        ("Reports generated", str(len(reports_data)), "From MAO executions", "cyan"),
        ("Resolved incidents", str(sum(1 for r in reports_data if r.get("success"))), "Successful workflows", "green"),
        ("Average confidence", f"{round(sum(r.get('confidence', 0) for r in reports_data) / len(reports_data) * 100, 1)}%" if reports_data else "N/A", "Execution quality", "green"),
        ("Pending review", str(sum(1 for r in reports_data if not r.get("success"))), "Requires attention", "amber"),
    ]
    
    return {
        "metrics": metrics,
        "reports": formatted_reports,
        "preview": preview,
    }
```

## backend/api/adapters/frontend_services/telemetry_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/telemetry_adapter.py`

```python
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def get_asset_telemetry(asset_id):
    kernel = runtime.kernel
    readings = kernel.state.get_history(asset_id)

    history = []

    for reading in readings:
        history.append(
            {
                "Timestamp": reading.timestamp,
                "Sensor": reading.sensor_type,
                "Value": reading.value,
                "Unit": reading.unit,
            }
        )

    return {
        "history": history,
        "latest": history[-1] if history else None,
    }
```
