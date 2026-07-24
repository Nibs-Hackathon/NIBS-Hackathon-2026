"""Dynamic asset-risk prediction agent with Gemini-generated thresholds."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class PredictionAgent(Agent):
    """Estimate health and risk from telemetry using dynamic thresholds."""

    name = "prediction"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        asset_id = getattr(context.event, "source", None) if context else None
        readings = context.state.get_history(asset_id) if (context and asset_id) else []
        health_service = context.health_service if context else None
        
        health = (
            health_service.calculate_health(readings)
            if health_service is not None and readings
            else 100.0
        )
        
        # ✅ Get dynamic thresholds for asset type
        asset_type = self._get_asset_type(context) or "Pump"
        thresholds = self.config.get_thresholds(asset_type)
        
        # Calculate degradation rate using dynamic thresholds
        degradation_rate = self._degradation_rate(readings, health_service, thresholds)
        
        # Dynamic failure probability calculation
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
            f"Asset type: {asset_type}",
            f"Thresholds used: {thresholds}",
        ]
        
        metadata = {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "health": round(health, 1),
            "failure_probability": failure_probability,
            "rul_days": rul_days,
            "confidence": confidence,
            "evidence": evidence,
            "thresholds": thresholds,  # ✅ Track thresholds used
            "method": "deterministic_telemetry_heuristic_with_gemini_thresholds",
        }
        
        if context:
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
                f"Dynamic prediction completed: health {round(health, 1)}%, "
                f"failure probability {failure_probability}%, RUL {rul_days} day(s)."
            ),
        )

    def _get_asset_type(self, context):
        """Extract asset type from context."""
        if not context:
            return None
        
        if isinstance(context, dict):
            return context.get("asset_type")
        
        # Try to get from metadata
        if hasattr(context, "metadata"):
            sensor_metadata = context.metadata.get("sensor", {})
            return sensor_metadata.get("asset_type")
        
        # Try from event payload
        event = getattr(context, "event", None)
        if event:
            payload = getattr(event, "payload", {})
            return payload.get("asset_type")
        
        return None

    @staticmethod
    def _degradation_rate(readings, health_service, thresholds) -> float:
        """Calculate degradation rate using dynamic thresholds."""
        if len(readings) < 2 or health_service is None:
            return 0.25
        
        # Use thresholds to weight degradation
        baseline = health_service.calculate_health(readings[:1])
        current = health_service.calculate_health(readings)
        raw_rate = (baseline - current) / (len(readings) - 1)
        
        # Apply threshold-based adjustment
        adjustment = 1.0
        for reading in readings:
            sensor_type = reading.sensor_type.value if hasattr(reading.sensor_type, 'value') else str(reading.sensor_type)
            value = reading.value
            
            if "pressure" in sensor_type.lower():
                if value > thresholds.get("pressure_max", 150):
                    adjustment = 1.5
            elif "temperature" in sensor_type.lower():
                if value > thresholds.get("temperature_max", 85):
                    adjustment = 1.3
            elif "gas" in sensor_type.lower():
                if value > thresholds.get("gas_max", 40):
                    adjustment = 1.8
            elif "vibration" in sensor_type.lower():
                if value > thresholds.get("vibration_max", 8):
                    adjustment = 1.4
        
        return max(0.25, raw_rate * adjustment)

    @staticmethod
    def _recommendations(failure_probability: int) -> list[str]:
        if failure_probability >= 70:
            return ["Escalate for immediate engineering review."]
        if failure_probability >= 40:
            return ["Plan a maintenance inspection during the next safe window."]
        return ["Continue monitoring telemetry for trend changes."]