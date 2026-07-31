"""Asset health detail for the object inspector."""

from __future__ import annotations

from services.runtime import runtime


def get_asset_health(asset_id: str) -> dict:
    """Return identity, health, and recent readings for one asset."""
    kernel = runtime.kernel
    asset = kernel.asset_service.get(asset_id)
    if asset is None:
        return {
            "id": asset_id,
            "data_available": False,
            "message": "Asset not found in the live asset registry.",
        }

    readings = kernel.state.get_history(asset_id) or []
    health = kernel.health.calculate_health(readings) if readings else float(getattr(asset, "health", 0) or 0)
    latest_by_sensor: dict[str, dict] = {}
    for reading in readings[-40:]:
        sensor = getattr(getattr(reading, "sensor_type", None), "value", None) or str(
            getattr(reading, "sensor_type", "unknown")
        )
        latest_by_sensor[sensor] = {
            "sensor_type": sensor,
            "value": float(getattr(reading, "value", 0) or 0),
            "unit": getattr(reading, "unit", "") or "",
            "timestamp": reading.timestamp.isoformat() if getattr(reading, "timestamp", None) else None,
        }

    asset_type = getattr(asset, "asset_type", None)
    type_value = getattr(asset_type, "value", None) or str(asset_type or "Unknown")

    return {
        "id": asset.id,
        "name": asset.name,
        "type": type_value,
        "location": getattr(asset, "location", None),
        "zone": getattr(asset, "zone", None),
        "refinery_id": getattr(asset, "refinery_id", None),
        "health": round(float(health), 1),
        "status": getattr(asset, "status", None)
        or ("Running" if health > 80 else "Warning" if health > 50 else "Critical"),
        "data_available": True,
        "readings_count": len(readings),
        "signals": latest_by_sensor,
        "temperature": (latest_by_sensor.get("Temperature") or {}).get("value"),
        "pressure": (latest_by_sensor.get("Pressure") or {}).get("value"),
        "vibration": (latest_by_sensor.get("Vibration") or {}).get("value"),
        "last_reading_at": next(
            (row["timestamp"] for row in reversed(list(latest_by_sensor.values())) if row.get("timestamp")),
            None,
        ),
        "readings": [
            {
                "sensor_type": getattr(getattr(r, "sensor_type", None), "value", str(getattr(r, "sensor_type", ""))),
                "value": float(getattr(r, "value", 0) or 0),
                "unit": getattr(r, "unit", "") or "",
                "timestamp": r.timestamp.isoformat() if getattr(r, "timestamp", None) else None,
            }
            for r in readings[-20:]
        ],
    }
