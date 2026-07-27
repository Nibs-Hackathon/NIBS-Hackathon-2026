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
from mao.models.task import TaskStatus
from mao.workflows.pressure_workflow import PressureWorkflow


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


def test_pressure_spike_runs_agents_in_dependency_order():
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
        stack.enter_context(
            patch("mao.kernel.PersistenceService", return_value=persistence)
        )
        stack.enter_context(
            patch("mao.kernel.HealthService", return_value=MagicMock())
        )
        for target in config_targets:
            stack.enter_context(patch(target, return_value=config))

        kernel = MAOKernel()
        kernel.register_workflow(PressureWorkflow())

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
        payload={"asset_type": "Pump", "pressure": 170},
    )

    report = kernel.handle_event(event)

    assert report.success is True
    assert report.workflow_name == "pressure_response"
    assert report.total_agents == len(AGENT_ORDER)
    assert [result.agent_name for result in report.agent_results] == AGENT_ORDER
    scheduled_tasks = sorted(kernel.state.tasks, key=lambda task: task.priority)
    assert [task.assigned_agent for task in scheduled_tasks] == AGENT_ORDER
    assert all(task.status == TaskStatus.COMPLETED for task in kernel.state.tasks)

    assert report.metadata["diagnosis"]["diagnosis"] == ["Pressure surge"]
    assert report.metadata["maintenance"]["priority"] == "HIGH"
    assert "Stabilize system pressure." in (
        report.metadata["planning"]["execution_plan"]
    )
    assert report.metadata["knowledge"]["query"] == "Pressure surge"
    assert report.metadata["report"]["source_agents"] == AGENT_ORDER[:-1]
    assert report.metadata["incident_id"] == event.id
    assert all(
        result.metadata["incident_id"] == event.id
        for result in report.agent_results
    )

    assert kernel.event_store.all() == [event]
    assert kernel.state.events == [event]
    assert kernel.state.execution_reports == [report]
    persistence.record_execution.assert_called_once_with(event, report)
