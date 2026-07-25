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