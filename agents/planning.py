"""
agents/planning.py

Production Planning Agent

Responsibilities
----------------
- Build an operational response plan
- Prioritize maintenance actions
- Recommend execution sequence
- Publish planning metadata
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class PlanningAgent(Agent):

    name = "planning"

    def execute(self, task, context):

        safety = self._get_metadata(context, "safety")
        diagnosis = self._get_metadata(context, "diagnosis")
        maintenance = self._get_metadata(context, "maintenance")

        status = safety.get("status", "SAFE")
        findings = diagnosis.get("diagnosis", [])
        work_orders = maintenance.get("work_orders", [])
        priority = maintenance.get("priority", "LOW")

        execution_plan = []

        if status == "CRITICAL":
            execution_plan.append(
                "Immediately reduce operating load."
            )
            execution_plan.append(
                "Notify control room."
            )

        if "Possible gas leak" in findings:
            execution_plan.append(
                "Isolate affected pipeline section."
            )

        if "Pressure surge" in findings:
            execution_plan.append(
                "Stabilize system pressure."
            )

        if "Equipment overheating" in findings:
            execution_plan.append(
                "Start cooling procedure."
            )

        execution_plan.extend(work_orders)

        if not execution_plan:
            execution_plan.append(
                "Continue normal operation."
            )

        estimated_duration = self._estimate_duration(priority)

        metadata = {
            "priority": priority,
            "execution_plan": execution_plan,
            "estimated_duration": estimated_duration,
            "status": status,
        }

        self._store_metadata(
            context,
            metadata,
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Execution plan created ({priority} priority)",
            confidence=0.96,
            evidence=execution_plan,
            recommendations=execution_plan,
            required_action="Execute plan",
            requires_human_approval=(
                status == "CRITICAL"
            ),
            metadata=metadata,
            summary=(
                f"Operational plan generated with "
                f"{len(execution_plan)} step(s)."
            ),
        )

    def _estimate_duration(self, priority):

        mapping = {
            "LOW": "15-30 minutes",
            "MEDIUM": "30-60 minutes",
            "HIGH": "1-3 hours",
            "CRITICAL": "Immediate",
        }

        return mapping.get(priority, "Unknown")

    def _get_metadata(self, context, key):

        if isinstance(context, dict):
            return context.get("metadata", {}).get(key, {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get(key, {})

    def _store_metadata(self, context, metadata):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["planning"] = metadata

            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["planning"] = metadata