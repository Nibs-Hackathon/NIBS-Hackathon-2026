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