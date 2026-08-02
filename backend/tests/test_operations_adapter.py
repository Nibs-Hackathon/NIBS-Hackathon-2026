from datetime import datetime
from types import SimpleNamespace

from api.adapters import operations_adapter
from services.notification_service import (
    Notification,
    NotificationSeverity,
    NotificationType,
    notification_service,
)


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


def test_notifications_include_asset_refinery_and_incident_detail(monkeypatch):
    monkeypatch.setattr(notification_service, "_notifications", [
        Notification(
            id="notification-1",
            type=NotificationType.INCIDENT_DETECTED,
            severity=NotificationSeverity.CRITICAL,
            title="Pipeline P-002 · Mumbai Coastal Refinery",
            message="Pressure spike",
            asset_id="asset-1",
            asset_name="Pipeline P-002",
            refinery_name="Mumbai Coastal Refinery",
            incident_type="Pressure spike",
        )
    ])

    payload = operations_adapter._notifications()[0]

    assert payload["type"] == "incident_detected"
    assert payload["asset_name"] == "Pipeline P-002"
    assert payload["refinery_name"] == "Mumbai Coastal Refinery"
    assert payload["message"] == "Pressure spike"


def test_average_asset_health_skips_missing_readings():
    assert operations_adapter._average_asset_health([
        {"health": 90},
        {"health": None},
        {"health": "bad"},
        {"health": 70},
    ]) == 80.0
    assert operations_adapter._average_asset_health([{"health": None}]) is None


def test_published_asset_health_falls_back_when_history_missing():
    asset = SimpleNamespace(id="a1", health=88.4)
    kernel = SimpleNamespace(state=SimpleNamespace(get_history=lambda _id: []))
    assert operations_adapter._published_asset_health(asset, kernel) == 88.4


def test_published_asset_health_recomputes_from_telemetry():
    asset = SimpleNamespace(id="a1", health=100.0)
    kernel = SimpleNamespace(
        state=SimpleNamespace(get_history=lambda _id: [{"value": 1}] * 5),
        health=SimpleNamespace(calculate_health=lambda _readings: 61.2),
    )
    assert operations_adapter._published_asset_health(asset, kernel) == 61.2
