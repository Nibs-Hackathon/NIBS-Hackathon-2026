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
            get=lambda _asset_id: SimpleNamespace(name="Pipeline P-002", health=92)
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
