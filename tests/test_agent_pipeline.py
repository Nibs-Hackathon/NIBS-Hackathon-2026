from unittest.mock import MagicMock

from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent
from agents.planning import PlanningAgent
from agents.knowledge import KnowledgeAgent

from mao.models.task import Task


def test_pipeline(critical_context):

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
            name="Maintenance",
            description="Generate maintenance plan",
            assigned_agent="maintenance",
            priority=3,
        ),
        critical_context
    )

    PlanningAgent().run(
        Task(
            name="Planning",
            description="Generate execution plan",
            assigned_agent="planning",
            priority=4,
        ),
        critical_context
    )

    agent = KnowledgeAgent(
        MagicMock()
    )

    agent.retriever = MagicMock()

    agent.retriever.retrieve.return_value = []

    agent.run(
        Task(
            name="Knowledge",
            description="Retrieve knowledge",
            assigned_agent="knowledge",
            priority=5,
        ),
        critical_context
    )

    expected = [
        "safety",
        "diagnosis",
        "maintenance",
        "planning",
        "knowledge",
    ]

    for key in expected:
        assert key in critical_context.metadata