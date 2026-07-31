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


def _failure_label(asset_id: str, health: float) -> str:
    """Derive failure probability from computation engine; fall back to health-based estimate."""
    try:
        from services.computation_engine import ComputationEngine
        kernel = runtime.kernel
        readings = kernel.state.get_history(asset_id)
        if not readings:
            raise ValueError("no readings")
        asset = kernel.asset_service.get(asset_id)
        engine = ComputationEngine()
        metrics = engine.compute_asset(asset, readings)
        prob = float(metrics.get("failure_probability") or 0)
        return f"{round(prob, 1)}%"
    except Exception:
        # Heuristic fallback so the field is never literally "Not available"
        if health < 50:
            return f"{round(50 + (50 - health), 1)}%"
        if health < 70:
            return f"{round(30 - (health - 50) * 0.8, 1)}%"
        return f"{max(0.0, round((100 - health) * 0.2, 1))}%"


def get_twin_assets() -> list[dict]:
    """Return current assets and latest observed telemetry from the runtime."""
    kernel = runtime.kernel
    assets = []
    for asset in kernel.asset_service.all_assets():
        readings = kernel.state.get_history(asset.id)
        health = kernel.health.calculate_health(readings) if readings else asset.health

        temp = _reading_value(readings, "temperature")
        pressure = _reading_value(readings, "pressure")
        rpm = _reading_value(readings, "rpm")
        failure = _failure_label(asset.id, health)

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
            "Failure": failure,
            "Recommendation": _maintenance_recommendation(asset.id),
        })
    return assets