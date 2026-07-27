from types import SimpleNamespace
from unittest.mock import MagicMock

from models.sensor import SensorType
from services.incident_service import IncidentService
from simulator.event_generator import EventGenerator


def test_pressure_spike_api_name_targets_a_live_asset():
    simulator = MagicMock()
    simulator.active_incidents = {}
    simulator.facility.assets = [
        SimpleNamespace(asset=SimpleNamespace(id="asset-1")),
    ]
    simulator.tick.return_value = (["reading"], ["report"])

    result = IncidentService(simulator).trigger_incident("pressure_spike")

    call = simulator.tick.call_args.kwargs
    assert call["fault"] == {"sensor": SensorType.PRESSURE, "value": 155}
    assert call["target_asset_id"] == "asset-1"
    assert result == {
        "incident_type": "pressure spike",
        "asset_id": "asset-1",
        "telemetry_count": 1,
        "reports_count": 1,
    }


def test_pressure_sensor_enum_generates_pressure_spike_event():
    generator = EventGenerator()
    generator.add_fault(
        {"sensor": SensorType.PRESSURE, "value": 155},
        asset_id="asset-1",
        asset_type="Pump",
    )

    events = generator.generate([])

    assert len(events) == 1
    assert events[0].name == "PressureSpike"
    assert events[0].source == "asset-1"
    assert events[0].payload["pressure"] == 155
