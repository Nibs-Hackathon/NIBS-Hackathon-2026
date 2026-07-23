"""
agents/maintenance.py

Production Maintenance Agent

Responsibilities
----------------
- Review diagnostic findings
- Assess maintenance urgency
- Recommend maintenance actions
- Estimate downtime
- Publish maintenance metadata
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class MaintenanceAgent(Agent):

    name = "maintenance"

    def execute(self, task, context):

        diagnosis = self._get_metadata(
            context,
            "diagnosis",
        )

        safety = self._get_metadata(
            context,
            "safety",
        )

        findings = diagnosis.get(
            "diagnosis",
            [],
        )

        work_orders = []
        priority = "LOW"
        downtime = "None"

        if "Pressure surge" in findings:
            work_orders.append(
                "Inspect pressure relief system"
            )
            priority = "HIGH"
            downtime = "2-4 hours"

        if "Equipment overheating" in findings:
            work_orders.append(
                "Inspect cooling system"
            )
            priority = "HIGH"
            downtime = "3-5 hours"

        if "Possible gas leak" in findings:
            work_orders.append(
                "Emergency pipeline inspection"
            )
            priority = "CRITICAL"
            downtime = "Immediate shutdown"

        if "Mechanical wear" in findings:
            work_orders.append(
                "Replace worn bearings"
            )

            if priority != "CRITICAL":
                priority = "MEDIUM"

            downtime = "4-6 hours"

        if "Flow restriction" in findings:
            work_orders.append(
                "Inspect valves and clean pipeline"
            )

            if priority == "LOW":
                priority = "MEDIUM"

            downtime = "2 hours"

        if not work_orders:
            work_orders.append(
                "No maintenance required"
            )

        metadata = {
            "priority": priority,
            "downtime": downtime,
            "work_orders": work_orders,
            "risk_status": safety.get("status", "SAFE"),
        }

        self._store_metadata(
            context,
            metadata,
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Maintenance Priority: {priority}",
            confidence=0.95,
            evidence=work_orders,
            recommendations=work_orders,
            required_action=priority,
            requires_human_approval=(
                priority in ("HIGH", "CRITICAL")
            ),
            metadata=metadata,
            summary=(
                f"{len(work_orders)} maintenance task(s) "
                f"generated. Priority: {priority}."
            ),
        )

    def _get_metadata(
        self,
        context,
        key,
    ):

        if isinstance(context, dict):
            return context.get(
                "metadata",
                {},
            ).get(key, {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get(key, {})

    def _store_metadata(
        self,
        context,
        metadata,
    ):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["maintenance"] = metadata

            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["maintenance"] = metadata