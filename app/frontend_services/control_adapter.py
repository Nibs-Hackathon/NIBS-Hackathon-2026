"""Control adapter using BackendAPI."""

from app.frontend_services.backend_api import api


def get_control_state() -> dict:
    """Return a facility snapshot derived from live state."""
    assets = api.get_assets()
    incidents = api.get_incidents()
    status = api.get_simulation_status()
    
    if not assets:
        return {
            "facility_mode": "NO ASSETS",
            "throughput": "N/A",
            "safety": "0 / 0",
            "queue": "0",
            "zones": [],
            "summary": "No assets are registered with the shared MAO runtime.",
        }
    
    healthy_assets = [a for a in assets if a.get("status", "").lower() in {"running", "healthy"}]
    average_health = sum(a.get("health", 0) for a in assets) / len(assets) if assets else 0
    facility_mode = "RUNNING" if healthy_assets else "ATTENTION"
    
    # Group by zone
    zones: dict[str, dict] = {}
    for asset in assets:
        zone = asset.get("location", "Unassigned")
        zones.setdefault(zone, {"assets": 0, "health": []})
        zones[zone]["assets"] += 1
        zones[zone]["health"].append(asset.get("health", 0))
    
    zone_snapshot = []
    for name, data in sorted(zones.items()):
        average_zone_health = sum(data["health"]) / len(data["health"]) if data["health"] else 0
        zone_snapshot.append({
            "Zone": name,
            "State": "Nominal" if average_zone_health >= 80 else "Attention",
            "Health": f"{round(average_zone_health)}%",
            "Assets": data["assets"],
        })
    
    return {
        "facility_mode": facility_mode,
        "throughput": f"{round((len(healthy_assets) / len(assets)) * 100, 1)}%" if assets else "N/A",
        "safety": f"{len(healthy_assets)} / {len(assets)}",
        "queue": str(len(incidents)),
        "zones": zone_snapshot,
        "summary": f"{len(healthy_assets)} of {len(assets)} registered assets are operating normally; average asset health is {round(average_health, 1)}%.",
    }