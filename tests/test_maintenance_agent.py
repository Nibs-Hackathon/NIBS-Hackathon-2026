from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent

from mao.models.task import Task


def test_maintenance_plan(critical_context):

    SafetyAgent().run(Task(
            name="Safety",
            description="Safety Assessment",
            assigned_agent="safety",
            priority=1,
        ),
        critical_context,
    )
    

    DiagnosticAgent().run(
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
            
        ),
        critical_context,
    )

    result = MaintenanceAgent().run(
        Task(
            name="Maintenance",
            description="Generate maintenance plan",
            assigned_agent="maintenance",
            priority=3,
        ),
        critical_context,
    )

    assert result.success

    metadata = critical_context.metadata["maintenance"]

    assert "priority" in metadata

    assert "work_orders" in metadata

    assert len(metadata["work_orders"]) > 0