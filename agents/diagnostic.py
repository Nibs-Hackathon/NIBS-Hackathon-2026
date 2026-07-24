"""Production Diagnostic Agent with dynamic thresholds."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class DiagnosticAgent(Agent):
    """Diagnostic agent using Gemini-generated thresholds."""

    name = "diagnostic"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()
        self._thresholds_cache = {}

    def _get_thresholds(self, context):
        """Get thresholds for the asset type."""
        asset_type = self._get_asset_type(context) or "Pump"
        cache_key = f"thresholds_{asset_type}"
        if cache_key in self._thresholds_cache:
            return self._thresholds_cache[cache_key]
        
        thresholds = self.config.get_thresholds(asset_type)
        self._thresholds_cache[cache_key] = thresholds
        return thresholds

    def _get_asset_type(self, context):
        """Extract asset type from context."""
        if isinstance(context, dict):
            return context.get("asset_type")
        
        event = getattr(context, "event", None)
        if event:
            payload = getattr(event, "payload", {})
            return payload.get("asset_type")
        
        return None

    def execute(self, task, context):
        telemetry = self._extract_telemetry(context)
        safety = self._get_safety(context)
        thresholds = self._get_thresholds(context)

        pressure = telemetry.get("pressure", 0)
        temperature = telemetry.get("temperature", 0)
        gas = telemetry.get("gas_level", telemetry.get("gas", 0))
        vibration = telemetry.get("vibration", 0)
        flow = telemetry.get("flow_rate", 0)

        diagnosis = []
        evidence = []

        # ✅ Dynamic thresholds from Gemini
        if pressure >= thresholds.get("pressure_max", 150):
            diagnosis.append("Pressure surge")
            evidence.append("Pressure exceeded safe operating threshold.")

        if temperature >= thresholds.get("temperature_max", 85):
            diagnosis.append("Equipment overheating")
            evidence.append("Temperature above recommended operating range.")

        if gas >= thresholds.get("gas_max", 40):
            diagnosis.append("Possible gas leak")
            evidence.append("Gas concentration indicates potential leak.")

        if vibration >= thresholds.get("vibration_max", 8):
            diagnosis.append("Mechanical wear")
            evidence.append("High vibration suggests bearing or shaft wear.")

        if flow and flow <= thresholds.get("flow_min", 25):
            diagnosis.append("Flow restriction")
            evidence.append("Low flow rate indicates blockage or valve restriction.")

        if not diagnosis:
            diagnosis.append("System operating normally")

        confidence = 0.95 if safety.get("status") != "SAFE" else 0.90

        recommendations = []
        if "Pressure surge" in diagnosis:
            recommendations.append("Inspect pressure relief valve.")
        if "Equipment overheating" in diagnosis:
            recommendations.append("Check cooling system.")
        if "Possible gas leak" in diagnosis:
            recommendations.append("Inspect pipelines and gas sensors.")
        if "Mechanical wear" in diagnosis:
            recommendations.append("Inspect rotating equipment.")
        if "Flow restriction" in diagnosis:
            recommendations.append("Inspect valves and pipelines.")
        if not recommendations:
            recommendations.append("Continue monitoring.")

        metadata = {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "evidence": evidence,
            "thresholds": thresholds,  # ✅ Track thresholds used
            "source": "DiagnosticAgent",
        }

        self._store_metadata(context, metadata)

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=", ".join(diagnosis),
            confidence=confidence,
            evidence=evidence,
            recommendations=recommendations,
            required_action="Maintenance inspection" if diagnosis != ["System operating normally"] else "None",
            requires_human_approval=False,
            metadata=metadata,
            summary=f"Diagnosis complete: {', '.join(diagnosis)}",
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

    def _get_safety(self, context):
        if isinstance(context, dict):
            return context.get("metadata", {}).get("safety", {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get("safety", {})

    def _store_metadata(self, context, metadata):
        if isinstance(context, dict):
            context.setdefault("metadata", {})["diagnosis"] = metadata
            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["diagnosis"] = metadata