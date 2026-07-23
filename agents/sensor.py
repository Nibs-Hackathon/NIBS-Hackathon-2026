"""Sensor observation agent for metadata enrichment only."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class SensorAgent(Agent):
    """Summarize telemetry already accepted by the runtime.

    The agent deliberately does not generate events. EventGenerator remains the
    single incident-generation mechanism.
    """

    name = "sensor"

    def execute(self, task, context):
        event = getattr(context, "event", None)
        payload = getattr(event, "payload", {}) or {}
        asset_id = getattr(event, "source", None)
        readings = context.state.get_history(asset_id) if asset_id else []

        signals = [
            f"{signal}: {value}"
            for signal, value in payload.items()
        ]
        metadata = {
            "asset_id": asset_id,
            "event_name": getattr(event, "name", "Unknown"),
            "signals": dict(payload),
            "history_samples": len(readings),
            "anomaly_observed": bool(payload),
        }
        context.metadata["sensor"] = metadata

        finding = (
            f"Observed {len(signals)} telemetry signal(s) for the incoming event."
            if signals
            else "No telemetry values were attached to the incoming event."
        )
        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=finding,
            confidence=0.9 if signals else 0.5,
            evidence=signals,
            recommendations=["Continue the configured response workflow."],
            required_action="Telemetry metadata recorded",
            requires_human_approval=False,
            metadata=metadata,
            summary=(
                f"Sensor observation recorded with {len(readings)} history sample(s)."
            ),
        )
