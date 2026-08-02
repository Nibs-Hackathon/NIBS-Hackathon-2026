"""Production Safety Agent with dynamic thresholds."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class SafetyAgent(Agent):
    """Safety assessment agent using Gemini-generated thresholds."""

    name = "safety"

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
        
        # Try to get from event or metadata
        event = getattr(context, "event", None)
        if event:
            payload = getattr(event, "payload", {})
            return payload.get("asset_type")
        
        return None

    def _get_risk_weights(self, incident_type):
        """Get risk weights for the incident type."""
        return self.config.get_risk_weights(incident_type or "default")

    def execute(self, task, context):
        telemetry = self._extract_telemetry(context)
        thresholds = self._get_thresholds(context)
        weights = self._get_risk_weights(getattr(task, "name", "default"))

        pressure = telemetry.get("pressure", 0)
        temperature = telemetry.get("temperature", 0)
        gas = telemetry.get("gas_level", telemetry.get("gas", 0))
        vibration = telemetry.get("vibration", 0)
        flow = telemetry.get("flow", telemetry.get("flow_rate"))

        alerts = []
        risk_score = 0

        # ✅ Dynamic thresholds from Gemini
        if pressure >= thresholds.get("pressure_max", 150):
            alerts.append(f"High pressure detected ({pressure} PSI)")
            risk_score += weights.get("pressure_weight", 30)

        if temperature >= thresholds.get("temperature_max", 85):
            alerts.append(f"High temperature detected ({temperature} °C)")
            risk_score += weights.get("temperature_weight", 25)

        if gas >= thresholds.get("gas_max", 40):
            alerts.append(f"Gas concentration elevated ({gas})")
            risk_score += weights.get("gas_weight", 35)

        if vibration >= thresholds.get("vibration_max", 8):
            alerts.append(f"Abnormal vibration detected ({vibration})")
            risk_score += weights.get("vibration_weight", 20)

        if flow is not None and flow < thresholds.get("flow_min", 25):
            alerts.append(f"Restricted flow detected ({flow})")
            risk_score += weights.get("flow_weight", 25)

        risk_score = min(risk_score, 100)

        # Status based on risk score
        if risk_score >= 80:
            status = "CRITICAL"
        elif risk_score >= 40:
            status = "WARNING"
        else:
            status = "SAFE"

        # Hard trip: pressure / temperature / gas over envelope → isolate that asset.
        hard_trip = bool(
            pressure >= thresholds.get("pressure_max", 150)
            or temperature >= thresholds.get("temperature_max", 85)
            or gas >= thresholds.get("gas_max", 40)
        )

        asset_id = self._get_asset_id(context)
        refinery = self._get_refinery(context)

        # Recommendations based on status
        recommendations = []
        control_actions = []
        if status == "CRITICAL" or hard_trip:
            if hard_trip and status == "SAFE":
                status = "CRITICAL"
            target = asset_id or "affected asset"
            where = f" at {refinery}" if refinery else ""
            recommendations.extend([
                f"Shut off {target}{where} immediately",
                "Notify control room",
                "Inspect affected equipment after isolation",
            ])
            if asset_id:
                control_actions.append({
                    "type": "shut_off",
                    "asset_id": asset_id,
                    "refinery": refinery,
                    "reason": alerts[0] if alerts else "Critical threshold breach",
                })
            if hasattr(context, "requires_shutdown"):
                context.requires_shutdown = True
        elif status == "WARNING":
            recommendations.extend([
                "Increase monitoring frequency",
                "Schedule inspection",
            ])
        else:
            recommendations.append("Continue normal operation")

        metadata = {
            "status": status,
            "incident_type": getattr(getattr(context, "event", None), "name", "Unknown"),
            "risk_score": risk_score,
            "alerts": alerts,
            "telemetry": telemetry,
            "thresholds": thresholds,  # ✅ Track which thresholds were used
            "confidence": 0.96,
            "asset_id": asset_id,
            "refinery": refinery,
            "control_actions": control_actions,
        }

        self._store_metadata(context, metadata)

        summary = f"Safety assessment completed. Status: {status}. Risk Score: {risk_score}/100."
        finding = alerts[0] if alerts else "No safety issues detected."

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=finding,
            confidence=0.96,
            evidence=alerts,
            recommendations=recommendations,
            required_action="Shut off asset" if (status == "CRITICAL" or hard_trip) else "Continue monitoring",
            # Hard-trip shutoff is agent-executed in the simulator; WO still needs review.
            requires_human_approval=False if (status == "CRITICAL" or hard_trip) else (status == "WARNING"),
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

    def _get_asset_id(self, context):
        if isinstance(context, dict):
            event = context.get("event") or {}
            return context.get("asset_id") or (
                event.get("source") if isinstance(event, dict) else getattr(event, "source", None)
            )
        event = getattr(context, "event", None)
        return getattr(event, "source", None) if event is not None else None

    def _get_refinery(self, context):
        telemetry = self._extract_telemetry(context)
        if telemetry.get("refinery") or telemetry.get("location"):
            return telemetry.get("refinery") or telemetry.get("location")
        asset_id = self._get_asset_id(context)
        if not asset_id:
            return None
        try:
            from services.runtime import runtime
            asset = runtime.kernel.asset_service.get(asset_id)
            return getattr(asset, "location", None) if asset else None
        except Exception:
            return None

    def _store_metadata(self, context, metadata):
        if isinstance(context, dict):
            context.setdefault("metadata", {})["safety"] = metadata
            return

        if not hasattr(context, "metadata"):
            context.metadata = {}
        context.metadata["safety"] = metadata
