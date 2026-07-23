"""Runtime-only notification agent."""

from __future__ import annotations

from agents.base import Agent
from mao.models.notification import Notification
from mao.models.result import AgentResult


class NotificationAgent(Agent):
    """Create structured in-memory notifications from workflow metadata."""

    name = "notification"

    def execute(self, task, context):
        safety = context.metadata.get("safety", {})
        maintenance = context.metadata.get("maintenance", {})
        prediction = context.metadata.get("prediction", {})
        severity = self._severity(safety, maintenance, prediction)
        notifications = []

        if severity != "INFO":
            notification = Notification(
                source=self.name,
                severity=severity,
                summary=self._summary(severity, prediction),
                asset_id=getattr(context.event, "source", None),
                requires_human_approval=(severity == "CRITICAL"),
                metadata={
                    "safety_status": safety.get("status", "SAFE"),
                    "maintenance_priority": maintenance.get("priority", "LOW"),
                    "failure_probability": prediction.get("failure_probability", 0),
                },
            )
            context.state.add_notification(notification)
            notifications.append(notification)

        metadata = {
            "notification_count": len(notifications),
            "severity": severity,
            "notification_ids": [notification.id for notification in notifications],
            "notifications": [
                {
                    "id": notification.id,
                    "source": notification.source,
                    "severity": notification.severity,
                    "summary": notification.summary,
                    "asset_id": notification.asset_id,
                    "requires_human_approval": notification.requires_human_approval,
                    "metadata": notification.metadata,
                    "created_at": notification.created_at,
                }
                for notification in notifications
            ],
        }
        context.metadata["notification"] = metadata
        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=(
                f"Created {len(notifications)} runtime notification(s)."
            ),
            confidence=0.95,
            evidence=[notification.summary for notification in notifications],
            recommendations=(
                ["Review the runtime notification queue."]
                if notifications
                else ["No operator notification is required."]
            ),
            required_action="Review notification" if notifications else "None",
            requires_human_approval=severity == "CRITICAL",
            metadata=metadata,
            summary=(
                f"Notification evaluation completed with severity {severity}."
            ),
        )

    @staticmethod
    def _severity(safety, maintenance, prediction) -> str:
        if (
            safety.get("status") == "CRITICAL"
            or maintenance.get("priority") == "CRITICAL"
            or prediction.get("failure_probability", 0) >= 70
        ):
            return "CRITICAL"
        if (
            safety.get("status") == "WARNING"
            or maintenance.get("priority") == "HIGH"
            or prediction.get("failure_probability", 0) >= 40
        ):
            return "WARNING"
        return "INFO"

    @staticmethod
    def _summary(severity, prediction) -> str:
        probability = prediction.get("failure_probability", 0)
        return (
            f"{severity.title()} operational notification: predicted failure probability "
            f"is {probability}%."
        )
