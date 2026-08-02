"""Execute supervised agent control and maintenance planning actions.

Hackathon scope: commands mutate the in-memory simulator / ActionDB audit trail.
They never reach physical industrial equipment.
"""

from __future__ import annotations

from typing import Any


def _event_asset_id(context) -> str | None:
    event = getattr(context, "event", None)
    if event is None:
        return None
    return getattr(event, "source", None) or (event.get("source") if isinstance(event, dict) else None)


def _event_incident_id(context) -> str | None:
    event = getattr(context, "event", None)
    if event is None:
        return None
    return getattr(event, "id", None) or (event.get("id") if isinstance(event, dict) else None)


def apply_agent_actuation(context) -> dict[str, Any]:
    """Apply shutoff + maintenance plans derived from agent metadata.

    Safety CRITICAL → shut off the specific incident asset at its refinery.
    Maintenance HIGH/CRITICAL (or any planned WO list) → create work orders.
    """
    safety = (getattr(context, "metadata", {}) or {}).get("safety", {}) or {}
    maintenance = (getattr(context, "metadata", {}) or {}).get("maintenance", {}) or {}
    asset_id = _event_asset_id(context)
    incident_id = _event_incident_id(context)

    executed: list[dict[str, Any]] = []
    errors: list[str] = []

    should_shut_off = bool(getattr(context, "requires_shutdown", False)) or str(
        safety.get("status", "")
    ).upper() == "CRITICAL"

    if should_shut_off and asset_id:
        try:
            from api.adapters.control_adapter import shut_off_asset

            result = shut_off_asset(
                asset_id,
                reason=safety.get("alerts", ["Critical threshold breach"])[0]
                if safety.get("alerts")
                else "Critical safety threshold breach",
                agent_name="safety",
                incident_id=incident_id,
            )
            executed.append({"type": "shut_off", **result})
            context.requires_shutdown = True
        except Exception as error:  # pragma: no cover - defensive boundary
            errors.append(f"shut_off:{type(error).__name__}:{error}")

    priority = str(maintenance.get("priority", "LOW")).upper()
    planned = [
        wo
        for wo in (maintenance.get("work_orders") or [])
        if wo and wo != "No maintenance required"
    ]
    should_plan = bool(planned) and priority in {"MEDIUM", "HIGH", "CRITICAL"}

    if should_plan and asset_id:
        try:
            from api.adapters.maintenance_adapter import create_work_order

            priority_map = {
                "CRITICAL": "P1",
                "HIGH": "P1",
                "MEDIUM": "P2",
                "LOW": "P3",
            }
            for title in planned:
                wo = create_work_order(
                    asset_id=asset_id,
                    title=title,
                    priority=priority_map.get(priority, "P2"),
                    owner="MAO Maintenance Agent",
                    downtime=maintenance.get("downtime"),
                    note=f"Auto-planned after {priority} agent assessment",
                    incident_id=incident_id,
                )
                executed.append({"type": "plan_work_order", **wo})
        except Exception as error:  # pragma: no cover - DB may be unavailable in unit tests
            errors.append(f"plan_work_order:{type(error).__name__}:{error}")

    actuation = {
        "executed": executed,
        "errors": errors,
        "asset_id": asset_id,
        "incident_id": incident_id,
        "shut_off_requested": should_shut_off,
        "maintenance_planned": should_plan,
    }
    if hasattr(context, "metadata"):
        context.metadata["agent_actuation"] = actuation
    return actuation
