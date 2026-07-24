"""Asset adapter using BackendAPI."""

from app.frontend_services.backend_api import api


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