"""Agent shutoff + maintenance planning on pressure/temperature hard trips."""

from contextlib import ExitStack
from unittest.mock import MagicMock, patch

from agents.diagnostic import DiagnosticAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.notification import NotificationAgent
from agents.planning import PlanningAgent
from agents.prediction import PredictionAgent
from agents.report import ReportAgent
from agents.safety import SafetyAgent
from agents.sensor import SensorAgent
from mao import MAOKernel
from mao.events.event import Event
from mao.workflows.pressure_workflow import PressureWorkflow
from models.asset import Asset, AssetType
import services.runtime as runtime_module


AGENT_ORDER = [
    "sensor",
    "safety",
    "diagnostic",
    "maintenance",
    "planning",
    "knowledge",
    "prediction",
    "notification",
    "report",
]


def test_pressure_hard_trip_shuts_off_asset_and_plans_maintenance():
    config = MagicMock()
    config.get_thresholds.return_value = {
        "pressure_max": 150,
        "temperature_max": 85,
        "gas_max": 40,
        "vibration_max": 8,
        "flow_min": 25,
    }
    config.get_risk_weights.return_value = {
        "pressure_weight": 30,
        "temperature_weight": 25,
        "gas_weight": 35,
        "vibration_weight": 20,
        "flow_weight": 10,
    }
    config.get_priority_level.return_value = 2
    config.get_workflow_sequence.return_value = AGENT_ORDER

    persistence = MagicMock()
    vector_store = MagicMock()
    vector_store.similarity_search.return_value = []

    config_targets = [
        "agents.sensor.ConfigService",
        "agents.safety.ConfigService",
        "agents.diagnostic.ConfigService",
        "agents.maintenance.ConfigService",
        "agents.planning.ConfigService",
        "agents.prediction.ConfigService",
        "agents.notification.ConfigService",
        "agents.report.ConfigService",
    ]

    with ExitStack() as stack:
        stack.enter_context(patch("mao.kernel.PersistenceService", return_value=persistence))
        stack.enter_context(patch("mao.kernel.HealthService", return_value=MagicMock()))
        for target in config_targets:
            stack.enter_context(patch(target, return_value=config))
        create_wo = stack.enter_context(
            patch(
                "api.adapters.maintenance_adapter.create_work_order",
                return_value={
                    "id": "wo-1",
                    "title": "Inspect pressure relief system",
                    "status": "pending_approval",
                    "asset_id": "pump-a-01",
                },
            )
        )

        kernel = MAOKernel()
        kernel.register_workflow(PressureWorkflow())
        asset = Asset(
            id="pump-a-01",
            name="Pump A-01",
            asset_type=AssetType.PUMP,
            refinery_id="ref-1",
            location="Baytown Refinery",
            status="Running",
            health=92,
        )
        kernel.asset_service.register(asset)

        stack.enter_context(patch.object(runtime_module, "get_kernel", return_value=kernel))
        stack.enter_context(patch.object(runtime_module, "_simulator", None))

        for agent in (
            SensorAgent(),
            SafetyAgent(),
            DiagnosticAgent(),
            MaintenanceAgent(),
            PlanningAgent(),
            KnowledgeAgent(vector_store),
            PredictionAgent(),
            NotificationAgent(),
            ReportAgent(),
        ):
            kernel.register_agent(agent)

        event = Event(
            name="PressureSpike",
            source="pump-a-01",
            payload={"asset_type": "Pump", "pressure": 170, "location": "Baytown Refinery"},
        )
        report = kernel.handle_event(event)

    assert report.success is True
    actuation = report.metadata.get("agent_actuation") or {}
    executed_types = {item.get("type") for item in actuation.get("executed") or []}
    assert "shut_off" in executed_types
    assert asset.status == "Offline"
    assert create_wo.called
    assert any("shut off" in (rec or "").lower() for rec in report.recommendations)
