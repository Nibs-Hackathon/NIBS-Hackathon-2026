from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent
from agents.planning import PlanningAgent

from mao.models.task import Task


def test_plan_generation(critical_context):

    SafetyAgent().run(
        Task(
            name="Safety",
            description="Safety Assessment",
            assigned_agent="safety",
            priority=1,
        ),
        critical_context
    )

    DiagnosticAgent().run(
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
        ),
        critical_context
    )

    MaintenanceAgent().run(
  
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
        ),
        critical_context
    )

    result = PlanningAgent().run(
        Task(
            name="Planning",
            description="Generate execution plan",
            assigned_agent="planning",
            priority=4,
        ),
        critical_context,   
    )

    assert result.success

    assert "planning" in critical_context.metadata

    plan = critical_context.metadata["planning"]

    assert len(plan["execution_plan"]) > 0