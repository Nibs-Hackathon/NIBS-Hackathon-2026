"""Production Maintenance Agent with dynamic priority levels."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class MaintenanceAgent(Agent):
    """Maintenance agent using Gemini-generated priorities."""

    name = "maintenance"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        diagnosis = self._get_metadata(context, "diagnosis")
        safety = self._get_metadata(context, "safety")

        findings = diagnosis.get("diagnosis", [])
        incident_type = getattr(task, "name", "default")

        work_orders = []
        priority = "LOW"
        downtime = "None"

        # ✅ Get priority from Gemini
        priority_level = self.config.get_priority_level(incident_type, safety.get("status", "Medium"))

        if "Pressure surge" in findings:
            work_orders.append("Inspect pressure relief system")
            if priority_level <= 2:
                priority = "HIGH"
            downtime = "2-4 hours"

        if "Equipment overheating" in findings:
            work_orders.append("Inspect cooling system")
            if priority_level <= 2:
                priority = "HIGH"
            downtime = "3-5 hours"

        if "Possible gas leak" in findings:
            work_orders.append("Emergency pipeline inspection")
            priority = "CRITICAL"
            downtime = "Immediate shutdown"

        if "Mechanical wear" in findings:
            work_orders.append("Replace worn bearings")
            if priority != "CRITICAL":
                priority = "MEDIUM"
            downtime = "4-6 hours"

        if "Flow restriction" in findings:
            work_orders.append("Inspect valves and clean pipeline")
            if priority == "LOW":
                priority = "MEDIUM"
            downtime = "2 hours"

        if not work_orders:
            work_orders.append("No maintenance required")

        # When safety already forced shutoff, keep a concrete follow-up WO.
        if safety.get("status") == "CRITICAL" and work_orders == ["No maintenance required"]:
            work_orders = ["Post-shutoff inspection and restart clearance"]
            priority = "CRITICAL"
            downtime = "Immediate shutdown"

        planned = [wo for wo in work_orders if wo != "No maintenance required"]
        # Audit fields share one list: planned WOs, or the explicit none marker.
        audit_orders = planned if planned else ["No maintenance required"]
        metadata = {
            "priority": priority,
            "priority_level": priority_level,
            "downtime": downtime,
            "work_orders": audit_orders,
            "planned_work_orders": planned,
            "auto_plan": bool(planned) and priority in ("MEDIUM", "HIGH", "CRITICAL"),
            "risk_status": safety.get("status", "SAFE"),
        }

        self._store_metadata(context, metadata)

        summary = (
            f"{len(planned)} maintenance task(s) planned. Priority: {priority}."
            if planned
            else f"No maintenance required. Priority: {priority}."
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Maintenance Priority: {priority}",
            confidence=0.95,
            evidence=audit_orders,
            recommendations=audit_orders,
            required_action=priority,
            # Plans are auto-created; field completion still needs human transition.
            requires_human_approval=(priority in ("HIGH", "CRITICAL")),
            metadata=metadata,
            summary=summary,
        )

    def _get_metadata(self, context, key):
        if isinstance(context, dict):
            return context.get("metadata", {}).get(key, {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get(key, {})

    def _store_metadata(self, context, metadata):
        if isinstance(context, dict):
            context.setdefault("metadata", {})["maintenance"] = metadata
            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["maintenance"] = metadata