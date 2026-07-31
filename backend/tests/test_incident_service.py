from types import SimpleNamespace
from unittest.mock import MagicMock

from models.asset import Asset, AssetType
from models.sensor import SensorType
from services.computation_engine import ComputationEngine
from services.incident_service import IncidentService
from simulator.asset import SimulatedAsset
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


def test_manual_scenario_stays_on_the_requested_facility_asset():
    simulator = MagicMock()
    simulator.active_incidents = {}
    simulator.facility.assets = [
        SimpleNamespace(asset=SimpleNamespace(id="texas-asset")),
        SimpleNamespace(asset=SimpleNamespace(id="mumbai-asset")),
    ]
    simulator.tick.return_value = (["reading"], ["report"])

    result = IncidentService(simulator).trigger_incident(
        "high_temperature",
        asset_id="mumbai-asset",
    )

    assert simulator.tick.call_args.kwargs["target_asset_id"] == "mumbai-asset"
    assert result["asset_id"] == "mumbai-asset"


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


def test_emergency_fault_changes_telemetry_and_asset_health():
    asset = Asset(
        id="compressor-1",
        name="Compressor C-03",
        asset_type=AssetType.COMPRESSOR,
        refinery_id="refinery-1",
        location="East Valley Refinery",
    )
    simulated = SimulatedAsset(asset)

    telemetry = simulated.tick(
        fault={"sensor": SensorType.VIBRATION, "value": 40},
    )
    vibration = next(
        reading
        for reading in telemetry
        if reading.sensor_type == SensorType.VIBRATION
    )
    metrics = ComputationEngine().compute_asset(asset, telemetry)

    assert vibration.value == 40
    assert metrics["health"] < 100
    assert metrics["status"] != "Running"


def test_injected_fault_recovers_to_the_original_baseline():
    asset = Asset(
        id="boiler-1",
        name="Boiler 003",
        asset_type=AssetType.BOILER,
        refinery_id="refinery-1",
        location="West Port Refinery",
    )
    simulated = SimulatedAsset(asset)
    original_flow = simulated.sensors[SensorType.FLOW]

    first = simulated.tick(
        fault={"sensor": SensorType.FLOW, "value": 15},
    )
    for _ in range(8):
        recovered = simulated.tick()

    first_flow = next(
        reading for reading in first if reading.sensor_type == SensorType.FLOW
    )
    recovered_flow = next(
        reading for reading in recovered if reading.sensor_type == SensorType.FLOW
    )

    assert first_flow.value == 15
    assert recovered_flow.value == round(original_flow, 2)
