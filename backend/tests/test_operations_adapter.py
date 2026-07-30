from datetime import datetime
from types import SimpleNamespace

from api.adapters import operations_adapter


def test_runtime_incident_includes_workflow_confidence(monkeypatch):
    event = SimpleNamespace(
        id="incident-1",
        timestamp=datetime(2026, 7, 27, 13, 10),
        source="asset-1",
        name="PressureSpike",
        payload={"pressure": 170},
    )
    report = SimpleNamespace(
        id="report-1",
        metadata={"incident_id": event.id},
        agent_results=[],
        average_confidence=0.94,
        recommendations=["Inspect the pressure control loop."],
        final_summary="Pressure spike investigated.",
        success=True,
    )
    kernel = SimpleNamespace(
        event_store=SimpleNamespace(all=lambda: [event]),
        state=SimpleNamespace(execution_reports=[report]),
        asset_service=SimpleNamespace(
            get=lambda _asset_id: SimpleNamespace(
                name="Pipeline P-002",
                health=92,
                location="Mumbai Coastal Refinery",
            )
        ),
    )
    monkeypatch.setattr(
        operations_adapter,
        "runtime",
        SimpleNamespace(kernel=kernel),
    )

    incident = operations_adapter._runtime_incidents(limit=10)[0]

    assert incident["confidence"] == 0.94
    assert incident["execution_report"]["confidence"] == 0.94
    assert incident["ai_recommendation"] == "Inspect the pressure control loop."
    assert incident["status"] == "resolved"
    assert incident["facility"] == "Mumbai Coastal Refinery"


def test_runtime_incident_tracks_live_simulator_state(monkeypatch):
    event = SimpleNamespace(
        id="incident-live",
        timestamp=datetime(2026, 7, 28, 10, 0),
        source="asset-1",
        name="FlowRestriction",
        payload={"flow": 15},
    )
    kernel = SimpleNamespace(
        event_store=SimpleNamespace(all=lambda: [event]),
        state=SimpleNamespace(execution_reports=[]),
        asset_service=SimpleNamespace(
            get=lambda _asset_id: SimpleNamespace(name="Boiler 003", health=95)
        ),
    )
    simulator = SimpleNamespace(
        active_incidents={"asset-1": {"event": event}},
    )
    monkeypatch.setattr(
        operations_adapter,
        "runtime",
        SimpleNamespace(kernel=kernel, active_simulator=simulator),
    )

    incident = operations_adapter._runtime_incidents(limit=10)[0]

    assert incident["status"] == "active"
    assert operations_adapter._sensor_from_incident(incident["incident_type"]) == "Flow"
