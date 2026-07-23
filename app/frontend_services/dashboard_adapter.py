from services.runtime import kernel



def calculate_severity(event):

    payload = event.payload


    if "gas" in payload:
        return "Critical"


    if "pressure" in payload:

        return (
            "Critical"
            if payload["pressure"] > 160
            else "High"
        )


    if "temperature" in payload:

        return (
            "Critical"
            if payload["temperature"] > 100
            else "High"
        )


    if "vibration" in payload:

        return (
            "Critical"
            if payload["vibration"] > 40
            else "High"
        )


    if "flow" in payload:
        return "Medium"


    return "Unknown"



def get_dashboard():

    # -------------------------
    # Assets
    # -------------------------

    assets = kernel.asset_service.all_assets()

    asset_snapshot = []

    for asset in assets:

        asset_snapshot.append(
            {
                "Asset": asset.name,
                "Type": asset.asset_type,
                "Zone": asset.location,
                "Health": asset.health,
                "Status": asset.status,
            }
        )


    # -------------------------
    # Incidents
    # -------------------------

    incidents = []

    for event in kernel.event_store.all():

        incidents.append(
            {
                "Incident": event.name,

                "Asset": event.source,

                "Severity": calculate_severity(event),

                "Detected": event.timestamp.strftime(
                    "%H:%M:%S"
                )
            }
        )


    # -------------------------
    # Metrics
    # -------------------------

    metrics = [
        (
            "Fleet health",
            calculate_average_health(assets),
            "Calculated from assets",
            "green"
        ),

        (
            "Assets online",
            f"{len(assets)} / {len(assets)}",
            "Connected",
            "cyan"
        ),

        (
            "Active incidents",
            str(len(incidents)),
            "From EventStore",
            "red"
        ),

        (
            "AI decisions",
            str(len(kernel.state.agent_results)),
            "Agent executions",
            "violet"
        )
    ]


    # -------------------------
    # Activity
    # -------------------------

    activity = []

    for report in kernel.state.execution_reports[-5:]:

        activity.append(
            (
                str(report.completed_at),
                "MAO",
                report.final_summary
            )
        )


    return {
        "metrics": metrics,
        "incidents": incidents,
        "assets": asset_snapshot,
        "activity": activity,
    }



def calculate_average_health(assets):

    if not assets:
        return "0%"

    value = sum(
        asset.health
        for asset in assets
    ) / len(assets)

    return f"{round(value,1)}%"