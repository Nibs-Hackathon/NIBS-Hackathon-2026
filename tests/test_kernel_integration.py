from unittest.mock import MagicMock

from agents.diagnostic import DiagnosticAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.planning import PlanningAgent
from agents.safety import SafetyAgent
from mao import MAOKernel
from mao.events.event import Event
from mao.workflows.pressure_workflow import PressureWorkflow


def test_pressure_spike_runs_through_kernel_end_to_end():
    kernel = MAOKernel()
    kernel.persistence = MagicMock()
    kernel.register_workflow(PressureWorkflow())

    vector_store = MagicMock()
    vector_store.get.return_value = None

    for agent in (
        SafetyAgent(),
        DiagnosticAgent(),
        KnowledgeAgent(vector_store),
        MaintenanceAgent(),
        PlanningAgent(),
    ):
        kernel.register_agent(agent)

    event = Event(
        name="PressureSpike",
        source="pump-a-01",
        payload={"pressure": 170},
    )

    report = kernel.handle_event(event)

    assert report.success is True
    assert report.workflow_name == "pressure_response"
    assert report.total_agents == 5
    assert report.successful_agents == 5
    assert report.failed_agents == 0
    assert [result.agent_name for result in report.agent_results] == [
        "safety",
        "diagnostic",
        "maintenance",
        "planning",
        "knowledge",
    ]
    assert report.metadata["safety"]["status"] == "SAFE"
    assert report.metadata["diagnosis"]["diagnosis"] == ["Pressure surge"]
    assert report.metadata["maintenance"]["priority"] == "HIGH"
    assert "Stabilize system pressure." in (
        report.metadata["planning"]["execution_plan"]
    )
    assert kernel.event_store.all() == [event]
    assert kernel.state.events == [event]
    assert kernel.state.execution_reports == [report]
    kernel.persistence.record_execution.assert_called_once_with(event, report)
