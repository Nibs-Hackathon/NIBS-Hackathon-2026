from agents.diagnostic import DiagnosticAgent
from agents.safety import SafetyAgent
from mao.models.task import Task


safety_task = Task(
    name="Safety",
    description="Safety Assessment",
    assigned_agent="safety",
    priority=1,
)

diag_task = Task(
    name="Diagnosis",
    description="Run diagnostics",
    assigned_agent="diagnostic",
    priority=2,
)

def test_diagnosis(critical_context):

    SafetyAgent().run(
        safety_task,
        critical_context,
    )

    result = DiagnosticAgent().run(
        diag_task,
        critical_context,
    )

    assert result.success

    assert "diagnosis" in critical_context.metadata

    diagnosis = critical_context.metadata["diagnosis"]

    assert len(diagnosis["diagnosis"]) > 0