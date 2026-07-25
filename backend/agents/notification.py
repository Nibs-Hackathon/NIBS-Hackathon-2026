"""Runtime notification agent with dynamic severity levels."""

from __future__ import annotations

from agents.base import Agent
from mao.models.notification import Notification
from mao.models.result import AgentResult
from services.config_services import ConfigService


class NotificationAgent(Agent):
    """Create structured in-memory notifications from workflow metadata."""

    name = "notification"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        safety = context.metadata.get("safety", {})
        maintenance = context.metadata.get("maintenance", {})
        prediction = context.metadata.get("prediction", {})
        
        # ✅ Get dynamic severity
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
                    "gemini_severity": severity,  # ✅ Track Gemini-generated severity
                },
            )
            context.state.add_notification(notification)
            notifications.append(notification)

        metadata = {
            "notification_count": len(notifications),
            "severity": severity,
            "notification_ids": [notification.id for notification in notifications],
        }
        context.metadata["notification"] = metadata
        
        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Created {len(notifications)} runtime notification(s).",
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
            summary=f"Notification evaluation completed with severity {severity}.",
        )

    def _severity(self, safety, maintenance, prediction) -> str:
        """Determine severity with dynamic thresholds."""
        failure_prob = prediction.get("failure_probability", 0)
        
        # Get incident type for dynamic thresholds
        incident_type = safety.get("incident_type", "default")
        
        # Get dynamic priority level
        priority_level = self.config.get_priority_level(incident_type, safety.get("status", "Medium"))
        
        # Critical if:
        # - Safety is CRITICAL
        # - Maintenance is CRITICAL
        # - Failure probability >= 70
        # - Gemini priority level <= 1 (Highest)
        if (
            safety.get("status") == "CRITICAL"
            or maintenance.get("priority") == "CRITICAL"
            or failure_prob >= 70
            or priority_level <= 1
        ):
            return "CRITICAL"
        
        # Warning if:
        # - Safety is WARNING
        # - Maintenance is HIGH
        # - Failure probability >= 40
        # - Gemini priority level <= 3
        if (
            safety.get("status") == "WARNING"
            or maintenance.get("priority") == "HIGH"
            or failure_prob >= 40
            or priority_level <= 3
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