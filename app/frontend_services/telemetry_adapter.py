from services.runtime import kernel


def get_asset_telemetry(asset_id):

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