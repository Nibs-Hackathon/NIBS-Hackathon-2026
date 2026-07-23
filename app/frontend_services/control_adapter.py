"""Read-only facility state for the Control Center page.

The adapter deliberately reads the process-wide runtime kernel rather than
creating a page-local MAO kernel.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel


def get_control_state() -> dict:
    """Return a facility snapshot derived from live MAO runtime state."""
    assets = kernel.asset_service.all_assets()
    events = kernel.event_store.all()

    if not assets:
        return {
            "facility_mode": "NO ASSETS",
            "throughput": "N/A",
            "safety": "0 / 0",
            "queue": str(len(events)),
            "zones": [],
            "summary": "No assets are registered with the shared MAO runtime.",
        }

    healthy_assets = [
        asset for asset in assets if asset.status.lower() in {"running", "healthy"}
    ]
    average_health = sum(asset.health for asset in assets) / len(assets)
    facility_mode = "RUNNING" if healthy_assets else "ATTENTION"

    zones: dict[str, dict] = {}
    for asset in assets:
        zone = asset.location or "Unassigned"
        zones.setdefault(zone, {"assets": 0, "health": []})
        zones[zone]["assets"] += 1
        zones[zone]["health"].append(asset.health)

    zone_snapshot = []
    for name, data in sorted(zones.items()):
        average_zone_health = sum(data["health"]) / len(data["health"])
        zone_snapshot.append(
            {
                "Zone": name,
                "State": "Nominal" if average_zone_health >= 80 else "Attention",
                "Health": f"{round(average_zone_health)}%",
                "Assets": data["assets"],
            }
        )

    return {
        "facility_mode": facility_mode,
        "throughput": f"{round((len(healthy_assets) / len(assets)) * 100, 1)}%",
        "safety": f"{len(healthy_assets)} / {len(assets)}",
        "queue": str(len(events)),
        "zones": zone_snapshot,
        "summary": (
            f"{len(healthy_assets)} of {len(assets)} registered assets are operating "
            f"normally; average asset health is {round(average_health, 1)}%."
        ),
    }
