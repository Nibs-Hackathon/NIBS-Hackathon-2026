"""Sensor observation agent with dynamic enrichment."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class SensorAgent(Agent):
    """Summarize telemetry with dynamic enrichment."""

    name = "sensor"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        event = getattr(context, "event", None)
        payload = getattr(event, "payload", {}) or {}
        asset_id = getattr(event, "source", None)
        readings = context.state.get_history(asset_id) if asset_id else []

        signals = [
            f"{signal}: {value}"
            for signal, value in payload.items()
        ]
        
        # ✅ Get dynamic thresholds for context
        asset_type = payload.get("asset_type", "Pump")
        thresholds = self.config.get_thresholds(asset_type)
        
        # Check if any signal exceeds thresholds
        anomalies = []
        for signal, value in payload.items():
            signal_lower = signal.lower()
            if "pressure" in signal_lower and value > thresholds.get("pressure_max", 150):
                anomalies.append(f"Pressure exceeds threshold: {value} > {thresholds.get('pressure_max')}")
            elif "temperature" in signal_lower and value > thresholds.get("temperature_max", 85):
                anomalies.append(f"Temperature exceeds threshold: {value} > {thresholds.get('temperature_max')}")
            elif "gas" in signal_lower and value > thresholds.get("gas_max", 40):
                anomalies.append(f"Gas exceeds threshold: {value} > {thresholds.get('gas_max')}")
            elif "vibration" in signal_lower and value > thresholds.get("vibration_max", 8):
                anomalies.append(f"Vibration exceeds threshold: {value} > {thresholds.get('vibration_max')}")
        
        metadata = {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "event_name": getattr(event, "name", "Unknown"),
            "signals": dict(payload),
            "history_samples": len(readings),
            "anomaly_observed": bool(payload),
            "anomalies": anomalies,
            "thresholds": thresholds,  # ✅ Track thresholds used
        }
        context.metadata["sensor"] = metadata

        finding = (
            f"Observed {len(signals)} telemetry signal(s) for the incoming event."
            + (f" Found {len(anomalies)} anomalies." if anomalies else " No anomalies detected.")
        )
        
        recommendations = []
        if anomalies:
            recommendations.append("Investigate anomalous readings.")
            recommendations.append("Refer to dynamic thresholds for guidance.")
        else:
            recommendations.append("Continue the configured response workflow.")
        
        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=finding,
            confidence=0.9 if signals else 0.5,
            evidence=signals + anomalies,
            recommendations=recommendations,
            required_action="Telemetry metadata recorded",
            requires_human_approval=bool(anomalies),
            metadata=metadata,
            summary=(
                f"Sensor observation recorded with {len(readings)} history sample(s). "
                f"Anomalies: {len(anomalies)}"
            ),
        )