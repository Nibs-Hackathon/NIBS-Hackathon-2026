"""Reusable intelligence stages appended to established operational workflows."""

from mao.models.task import Task


def intelligence_tasks() -> tuple[Task, Task, Task, Task]:
    """Return the common MAO intelligence stages with stable priorities."""
    return (
        Task(
            name="Sensor Observation",
            description="Record telemetry anomaly metadata without generating events.",
            assigned_agent="sensor",
            priority=1,
        ),
        Task(
            name="Failure Risk Prediction",
            description="Estimate deterministic health, failure probability, and RUL.",
            assigned_agent="prediction",
            priority=7,
        ),
        Task(
            name="Operator Notification",
            description="Create structured runtime notifications when escalation is needed.",
            assigned_agent="notification",
            priority=8,
        ),
        Task(
            name="Report Compilation",
            description="Compile agent outputs for the existing execution report.",
            assigned_agent="report",
            priority=9,
        ),
    )
