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