"""Live predictive-health view model using persisted PredictionAgent outputs."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import get_session
from database.repositories.prediction_repo import PredictionRepository
from frontend_services.demo_mode import demo_mode_enabled, sample_telemetry
from services.runtime import kernel


def _persisted_predictions(asset_id: str) -> tuple[list, str | None]:
    session = None
    try:
        session = get_session()
        return PredictionRepository(session).get_by_asset(asset_id), None
    except Exception:
        return [], "Prediction persistence is temporarily unavailable."
    finally:
        if session is not None:
            session.close()


def _historical_health(readings) -> list[float]:
    return [round(kernel.health.calculate_health(readings[: index + 1]), 1) for index in range(len(readings))]


def _telemetry_rows(readings) -> list[dict]:
    return [
        {
            "Sensor": getattr(reading.sensor_type, "value", str(reading.sensor_type)),
            "Observed": f"{reading.value} {getattr(reading, 'unit', '')}".strip(),
            "Time": reading.timestamp.strftime("%H:%M:%S"),
        }
        for reading in readings[-10:]
    ]


def get_health_prediction(asset_id: str, horizon_days: int = 14) -> dict:
    """Return only persisted predictions and observed runtime telemetry.

    ``horizon_days`` remains in the public adapter contract for UI selection, but
    it never manufactures a forecast. A future prediction run must persist a
    new PredictionAgent output for the selected horizon.
    """
    readings = kernel.state.get_history(asset_id)
    predictions, warning = _persisted_predictions(asset_id)
    latest = predictions[0] if predictions else None
    current_health = round(kernel.health.calculate_health(readings), 1) if readings else None
    evidence = list(latest.evidence or []) if latest else []
    demo = not readings and not predictions and demo_mode_enabled()

    telemetry = _telemetry_rows(readings)
    if demo:
        telemetry = sample_telemetry()

    return {
        "health": round(latest.health) if latest else current_health,
        "rul": f"{round(latest.rul_days, 1)} days" if latest else "Not available",
        "failure_probability": f"{round(latest.failure_probability * 100, 1)}%" if latest else "Not available",
        "confidence": f"{round(latest.confidence * 100, 1)}%" if latest else "Not available",
        "historical": {
            "Observed health": _historical_health(readings),
            "Prediction health": [round(prediction.health, 1) for prediction in reversed(predictions)],
        },
        "predicted": {
            "Prediction health": [round(prediction.health, 1) for prediction in reversed(predictions)],
            "Intervention threshold": [70] * len(predictions),
        },
        "telemetry": telemetry,
        "evidence": evidence,
        "warning": warning,
        "is_demo": demo,
        "has_prediction": latest is not None,
        "horizon_days": horizon_days,
    }
