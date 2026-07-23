from services.runtime import kernel, simulator
from services.incident_service import IncidentService


def trigger_incident(incident_type):

    service = IncidentService(
        simulator
    )

    return service.trigger_incident(
        incident_type
    )



def get_incidents():

    events = kernel.event_store.all()

    incidents = []

    for event in events:

        severity = calculate_severity(event)


        incidents.append(
            {
                "Incident": event.name,

                "Asset": event.source,

                "Severity": severity,

                "Detected": event.timestamp.strftime(
                    "%H:%M:%S"
                ),

                "Payload": event.payload,
            }
        )


    return incidents



def calculate_severity(event):

    payload = event.payload


    # derive severity from actual signal

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


    if "gas" in payload:

        return "Critical"


    if "vibration" in payload:

        return (
            "Critical"
            if payload["vibration"] > 40
            else "High"
        )


    if "flow" in payload:

        return "Medium"


    return "Unknown"