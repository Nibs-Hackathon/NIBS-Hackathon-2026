"""Deterministic asset-risk prediction agent."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class PredictionAgent(Agent):
    """Estimate health and risk from StateManager telemetry history.

    This intentionally uses deterministic heuristics. Its output contract is
    stable so a future statistical model can replace the implementation without
    changing workflow callers.
    """

    name = "prediction"

    def execute(self, task, context):
        asset_id = getattr(context.event, "source", None)
        readings = context.state.get_history(asset_id) if asset_id else []
        health_service = context.health_service
        health = (
            health_service.calculate_health(readings)
            if health_service is not None
            else 100.0
        )
        degradation_rate = self._degradation_rate(readings, health_service)
        failure_probability = (
            min(
                100,
                round(((100 - health) * 0.85) + min(20, degradation_rate * 4)),
            )
            if readings
            else 0
        )
        rul_days = (
            max(1, min(365, round(health / max(degradation_rate, 0.25))))
            if readings
            else 365
        )
        confidence = min(0.95, round(0.55 + min(len(readings), 20) * 0.02, 2))

        evidence = [
            f"Telemetry samples evaluated: {len(readings)}",
            f"Calculated health: {round(health, 1)}%",
            f"Observed degradation rate: {round(degradation_rate, 2)} health points/sample",
        ]
        metadata = {
            "asset_id": asset_id,
            "health": round(health, 1),
            "failure_probability": failure_probability,
            "rul_days": rul_days,
            "confidence": confidence,
            "evidence": evidence,
            "method": "deterministic_telemetry_heuristic",
        }
        context.metadata["prediction"] = metadata

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=(
                f"Failure probability is {failure_probability}% with an estimated "
                f"remaining useful life of {rul_days} day(s)."
            ),
            confidence=confidence,
            evidence=evidence,
            recommendations=self._recommendations(failure_probability),
            required_action=(
                "Schedule maintenance review" if failure_probability >= 40 else "Continue monitoring"
            ),
            requires_human_approval=failure_probability >= 70,
            metadata=metadata,
            summary=(
                f"Deterministic prediction completed: health {round(health, 1)}%, "
                f"failure probability {failure_probability}%, RUL {rul_days} day(s)."
            ),
        )

    @staticmethod
    def _degradation_rate(readings, health_service) -> float:
        if len(readings) < 2 or health_service is None:
            return 0.25
        baseline = health_service.calculate_health(readings[:1])
        current = health_service.calculate_health(readings)
        return max(0.25, (baseline - current) / (len(readings) - 1))

    @staticmethod
    def _recommendations(failure_probability: int) -> list[str]:
        if failure_probability >= 70:
            return ["Escalate for immediate engineering review."]
        if failure_probability >= 40:
            return ["Plan a maintenance inspection during the next safe window."]
        return ["Continue monitoring telemetry for trend changes."]
