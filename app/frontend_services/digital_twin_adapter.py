"""Read-only asset and telemetry view-model for the Digital Twin page."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel


def _reading_value(readings: list[Any], sensor_type: str) -> str:
    for reading in reversed(readings):
        reading_type = getattr(reading.sensor_type, "value", reading.sensor_type)
        if str(reading_type).lower() == sensor_type.lower():
            return f"{reading.value} {reading.unit}"
    return "Not available"


def _maintenance_recommendation(asset_id: str) -> str:
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
    """Return current assets and latest observed telemetry from the runtime.

    Failure probability is intentionally unavailable because HealthService does
    not expose a prediction model yet.
    TODO: Populate failure probability from the future prediction service.
    """
    assets = []
    for asset in kernel.asset_service.all_assets():
        readings = kernel.state.get_history(asset.id)
        health = kernel.health.calculate_health(readings) if readings else asset.health
        assets.append(
            {
                "id": asset.id,
                "Asset": asset.name,
                "Category": getattr(asset.asset_type, "value", str(asset.asset_type)),
                "Zone": asset.location or "Unassigned",
                "Status": asset.status or ("Healthy" if health >= 80 else "Attention"),
                "Health": round(health, 1),
                "Temperature": _reading_value(readings, "temperature"),
                "Pressure": _reading_value(readings, "pressure"),
                "RPM": _reading_value(readings, "rpm"),
                "Failure": "Not available",
                "Recommendation": _maintenance_recommendation(asset.id),
            }
        )
    return assets
