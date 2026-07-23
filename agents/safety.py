"""
agents/safety.py

Production Safety Agent

Responsibilities
----------------
- Analyze incoming telemetry
- Assess operational risk
- Detect safety threshold violations
- Publish safety metadata for downstream agents
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class SafetyAgent(Agent):

    name = "safety"

    PRESSURE_LIMIT = 150
    TEMPERATURE_LIMIT = 85
    GAS_LIMIT = 40
    VIBRATION_LIMIT = 8

    def execute(self, task, context):

        telemetry = self._extract_telemetry(context)

        pressure = telemetry.get("pressure", 0)
        temperature = telemetry.get("temperature", 0)
        gas = telemetry.get("gas_level", telemetry.get("gas", 0))
        vibration = telemetry.get("vibration", 0)

        alerts = []

        risk_score = 0

        if pressure >= self.PRESSURE_LIMIT:
            alerts.append(
                f"High pressure detected ({pressure} PSI)"
            )
            risk_score += 30

        if temperature >= self.TEMPERATURE_LIMIT:
            alerts.append(
                f"High temperature detected ({temperature} °C)"
            )
            risk_score += 25

        if gas >= self.GAS_LIMIT:
            alerts.append(
                f"Gas concentration elevated ({gas})"
            )
            risk_score += 35

        if vibration >= self.VIBRATION_LIMIT:
            alerts.append(
                f"Abnormal vibration detected ({vibration})"
            )
            risk_score += 20

        risk_score = min(risk_score, 100)

        if risk_score >= 80:
            status = "CRITICAL"

        elif risk_score >= 40:
            status = "WARNING"

        else:
            status = "SAFE"

        recommendations = []

        if status == "CRITICAL":

            recommendations.extend([
                "Reduce operating load immediately",
                "Notify control room",
                "Inspect affected equipment",
            ])

        elif status == "WARNING":

            recommendations.extend([
                "Increase monitoring frequency",
                "Schedule inspection",
            ])

        else:

            recommendations.append(
                "Continue normal operation"
            )

        metadata = {
            "status": status,
            "risk_score": risk_score,
            "alerts": alerts,
            "telemetry": telemetry,
            "confidence": 0.96,
        }

        self._store_metadata(
            context,
            metadata,
        )

        summary = (
            f"Safety assessment completed. "
            f"Status: {status}. "
            f"Risk Score: {risk_score}/100."
        )

        finding = (
            alerts[0]
            if alerts
            else "No safety issues detected."
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=finding,
            confidence=0.96,
            evidence=alerts,
            recommendations=recommendations,
            required_action=(
                "Immediate intervention"
                if status == "CRITICAL"
                else "Continue monitoring"
            ),
            requires_human_approval=(
                status == "CRITICAL"
            ),
            metadata=metadata,
            summary=summary,
        )

    def _extract_telemetry(self, context):

        if isinstance(context, dict):

            event = context.get("event")

            if isinstance(event, dict):
                return event.get("payload", {})

            return context.get("payload", {})

        event = getattr(context, "event", None)

        if event is None:
            return {}

        return getattr(event, "payload", {}) or {}

    def _store_metadata(
        self,
        context,
        metadata,
    ):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["safety"] = metadata

            return

        if not hasattr(context, "metadata"):

            context.metadata = {}

        context.metadata["safety"] = metadata
