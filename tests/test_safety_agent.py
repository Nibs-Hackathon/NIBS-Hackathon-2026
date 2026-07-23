from agents.safety import SafetyAgent
from mao.models.task import Task


task = Task(
    name="Safety",
    description="",
    assigned_agent="safety",
    priority=1,
)


def test_safe_system(normal_context):

    agent = SafetyAgent()

    result = agent.run(task, normal_context)

    assert result.success
    assert result.confidence > 0

    assert "safety" in normal_context.metadata

    assert (
        normal_context.metadata["safety"]["status"]
        == "SAFE"
    )


def test_critical_system(critical_context):

    agent = SafetyAgent()

    result = agent.run(task, critical_context)

    assert result.success

    metadata = critical_context.metadata["safety"]

    assert metadata["status"] == "CRITICAL"

    assert metadata["risk_score"] >= 80

    assert len(metadata["alerts"]) > 0