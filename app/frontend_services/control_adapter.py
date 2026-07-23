from services.runtime import kernel


def get_control_state():

    assets = kernel.asset_service.all_assets()

    if not assets:
        return {
            "facility_mode": "UNKNOWN",
            "throughput": "N/A",
            "safety": "0 / 0",
            "queue": "0",
            "zones": []
        }


    healthy = sum(
        1
        for asset in assets
        if asset.status in ["Running", "Healthy"]
    )


    zones = {}

    for asset in assets:

        zone = asset.location

        if zone not in zones:
            zones[zone] = {
                "assets": 0,
                "health": []
            }

        zones[zone]["assets"] += 1
        zones[zone]["health"].append(asset.health)


    zone_snapshot = []

    for name, data in zones.items():

        avg_health = (
            sum(data["health"])
            /
            len(data["health"])
        )

        state = (
            "Nominal"
            if avg_health > 80
            else "Attention"
        )

        zone_snapshot.append(
            {
                "Zone": name,
                "State": state,
                "Load": f"{round(avg_health)}%",
                "Assets": data["assets"]
            }
        )


    return {
        "facility_mode": "RUNNING",

        "throughput": f"{round((healthy/len(assets))*100,1)}%",

        "safety": f"{healthy} / {len(assets)}",

        "queue": str(
            len(kernel.event_store.all())
        ),

        "zones": zone_snapshot
    }