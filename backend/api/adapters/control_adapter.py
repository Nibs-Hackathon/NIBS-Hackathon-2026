"""Control adapter using BackendAPI."""

from __future__ import annotations

from typing import Any

from api.adapters.backend_api_new import api


def shut_off_asset(
    asset_id: str,
    *,
    reason: str = "Critical threshold breach",
    agent_name: str = "safety",
    incident_id: str | None = None,
) -> dict[str, Any]:
    """Shut off one simulated asset at its refinery.

    Updates runtime AssetService status to Offline, clears the active fault on
    the matching SimulatedAsset when present, and writes an ActionDB audit row
    when PostgreSQL is available. Never commands physical equipment.
    """
    from uuid import uuid4

    from services.runtime import runtime

    asset = runtime.kernel.asset_service.get(asset_id)
    if asset is None:
        return {
            "ok": False,
            "asset_id": asset_id,
            "message": "Asset not found in runtime; shutoff skipped.",
        }

    refinery = getattr(asset, "location", None) or getattr(asset, "refinery_id", None)
    asset_name = getattr(asset, "name", asset_id)
    runtime.kernel.asset_service.update_status(asset_id, "Offline")
    runtime.kernel.asset_service.update_health(
        asset_id, min(float(getattr(asset, "health", 100) or 100), 35.0)
    )

    # Only touch the already-running timer simulator; never spin up a new one here.
    simulator = runtime.active_simulator
    if simulator is not None:
        facility = getattr(simulator, "facility", None)
        if facility is not None:
            for simulated in getattr(facility, "assets", []) or []:
                if getattr(getattr(simulated, "asset", None), "id", None) == asset_id:
                    clear = getattr(simulated, "clear_fault", None)
                    if callable(clear):
                        clear()
                    else:
                        simulated._fault_active = False
                        simulated._fault_sensor = None
                        simulated._fault_original_value = None
                        simulated._fault_target_value = None
                        simulated._fault_ticks = 0
                    break
            active_faults = getattr(facility, "active_faults", None)
            if isinstance(active_faults, dict):
                active_faults.pop(asset_id, None)
        active = getattr(simulator, "active_incidents", None)
        if isinstance(active, dict) and asset_id in active:
            active[asset_id]["asset_status"] = "Offline"
            active[asset_id]["agent_shut_off"] = True

    action_id = None
    try:
        from database.connection import get_session
        from database.models import ActionDB
        from datetime import datetime, timezone

        session = get_session()
        try:
            action = ActionDB(
                id=str(uuid4()),
                incident_id=incident_id,
                asset_id=asset_id,
                action_type="agent_shutoff",
                payload={
                    "reason": reason,
                    "asset_name": asset_name,
                    "refinery": refinery,
                    "agent": agent_name,
                    "command": "shut_off",
                    "simulated": True,
                },
                risk_level="CRITICAL",
                status="executed",
                requires_human_approval=False,
                requested_by=f"MAO {agent_name}",
                approved_by=f"MAO {agent_name}",
                executed_at=datetime.now(timezone.utc),
            )
            session.add(action)
            session.commit()
            action_id = action.id
        finally:
            session.close()
    except Exception:
        action_id = None

    try:
        from services.notification_service import notification_service
        from services.notification_service import Notification, NotificationSeverity, NotificationType

        notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.INCIDENT_DETECTED,
                severity=NotificationSeverity.CRITICAL,
                title=" · ".join(v for v in (asset_name, refinery) if v),
                message=f"Agent shut off: {reason}",
                asset_id=asset_id,
                asset_name=asset_name,
                refinery_name=refinery,
                incident_type="AgentShutOff",
                metadata={"incident_id": incident_id, "action_id": action_id},
            )
        )
    except Exception:
        pass

    return {
        "ok": True,
        "asset_id": asset_id,
        "asset_name": asset_name,
        "refinery": refinery,
        "status": "Offline",
        "action_id": action_id,
        "message": (
            f"Simulated shutoff executed for {asset_name}"
            + (f" at {refinery}" if refinery else "")
            + f". Reason: {reason}"
        ),
    }


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