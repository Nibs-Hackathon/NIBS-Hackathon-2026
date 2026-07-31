"""Health prediction using computation engine."""

from __future__ import annotations

from services.runtime import runtime
from services.computation_engine import ComputationEngine


def get_health_prediction(asset_id, horizon_days=14, stress: float = 0.0):
    """Get health prediction using the computation engine.

    ``stress`` is a 0..1 operating-load factor. Higher stress accelerates
    degradation for what-if scenarios (heuristic, labeled in the response).
    """
    kernel = runtime.kernel
    engine = ComputationEngine()

    readings = kernel.state.get_history(asset_id)
    asset = kernel.asset_service.get(asset_id)
    stress_clamped = max(0.0, min(float(stress or 0.0), 1.0))
    stress_multiplier = 1.0 + (stress_clamped * 2.0)  # 1x .. 3x degradation

    if not asset or not readings:
        return {
            "asset_id": asset_id,
            "data_available": False,
            "health": None,
            "rul": None,
            "failure_probability": None,
            "confidence": None,
            "forecast_method": "unavailable: insufficient telemetry history",
            "stress": stress_clamped,
            "stress_multiplier": stress_multiplier,
            "historical": {"Historical health": []},
            "predicted": {"Predicted health": [], "Intervention threshold": []},
            "scenario": None,
            "telemetry": [],
        }

    metrics = engine.compute_asset(asset, readings)

    # Keep the chart legible and the calculation bounded. The prior adapter
    # returned the entire historian and recalculated every prefix (O(n²)),
    # which visually compressed the 14-day stress scenario into a tiny tail.
    history_window = readings[-42:]
    historical = []
    for i in range(len(history_window)):
        h = engine._calculate_health(
            history_window[: i + 1],
            engine.config.get_thresholds(metrics["asset_type"]),
            {},
        )
        historical.append(round(h, 1))

    current_health = metrics["health"]
    degradation_rate = metrics["degradation_rate"] * stress_multiplier

    predicted = []
    for day in range(horizon_days):
        health = current_health - (degradation_rate * 5 * (day + 1))
        predicted.append(round(max(0, health), 1))

    # Stress-adjusted RUL / failure probability (heuristic)
    base_rul = float(metrics["rul_days"] or 0)
    adj_rul = base_rul / stress_multiplier if stress_multiplier else base_rul
    base_fail = float(metrics["failure_probability"] or 0)
    adj_fail = min(99.0, base_fail * (1.0 + stress_clamped * 1.5))

    if adj_rul >= 365:
        rul_str = "365+ days"
    else:
        rul_str = f"{int(adj_rul)} days"

    # Cost / downtime estimates from adjusted risk (hackathon heuristic)
    intervention_cost = round(12000 + (adj_fail * 450) + (stress_clamped * 8000))
    downtime_hours = round(2 + (adj_fail / 20) + (stress_clamped * 6), 1)
    production_impact_pct = round(min(12.0, adj_fail / 15 + stress_clamped * 2), 1)

    method = "health trend extrapolation from verified simulator telemetry"
    if stress_clamped > 0:
        method = f"{method}; stress={stress_clamped:.2f} (degradation ×{stress_multiplier:.2f})"

    return {
        "asset_id": asset_id,
        "data_available": True,
        "health": round(metrics["health"]),
        "rul": rul_str,
        "failure_probability": f"{adj_fail:.1f}%",
        "confidence": f"{metrics['confidence'] * 100:.1f}%",
        "forecast_method": method,
        "stress": stress_clamped,
        "stress_multiplier": round(stress_multiplier, 2),
        "historical": {"Historical health": historical},
        "predicted": {
            "Predicted health": predicted,
            "Intervention threshold": [70] * horizon_days,
        },
        "scenario": {
            "stress": stress_clamped,
            "estimated_intervention_cost_usd": intervention_cost,
            "estimated_downtime_hours": downtime_hours,
            "estimated_production_impact_pct": production_impact_pct,
            "method": "heuristic stress-scaled degradation and exposure",
        },
        "telemetry": format_telemetry(readings),
    }


def format_telemetry(readings):
    """Format telemetry for display."""
    data = []
    for reading in readings[-10:]:
        data.append({
            "Sensor": reading.sensor_type.value if hasattr(reading.sensor_type, "value") else str(reading.sensor_type),
            "Observed": reading.value,
            "Time": reading.timestamp.strftime("%H:%M:%S") if getattr(reading, "timestamp", None) else None,
        })
    return data
