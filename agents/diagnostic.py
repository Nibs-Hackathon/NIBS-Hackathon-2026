"""
agents/diagnostic.py

Production Diagnostic Agent

Responsibilities
----------------
- Analyze telemetry
- Use Safety Agent findings
- Determine probable root causes
- Publish diagnosis metadata
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class DiagnosticAgent(Agent):

    name = "diagnostic"

    def execute(self, task, context):

        telemetry = self._extract_telemetry(context)

        safety = self._get_safety(context)

        pressure = telemetry.get("pressure", 0)
        temperature = telemetry.get("temperature", 0)
        gas = telemetry.get("gas_level", 0)
        vibration = telemetry.get("vibration", 0)
        flow = telemetry.get("flow_rate", 0)

        diagnosis = []
        evidence = []

        # Pressure
        if pressure >= 150:
            diagnosis.append("Pressure surge")
            evidence.append(
                "Pressure exceeded safe operating threshold."
            )

        # Temperature
        if temperature >= 85:
            diagnosis.append("Equipment overheating")
            evidence.append(
                "Temperature above recommended operating range."
            )

        # Gas
        if gas >= 40:
            diagnosis.append("Possible gas leak")
            evidence.append(
                "Gas concentration indicates potential leak."
            )

        # Vibration
        if vibration >= 8:
            diagnosis.append("Mechanical wear")
            evidence.append(
                "High vibration suggests bearing or shaft wear."
            )

        # Flow
        if flow and flow <= 25:
            diagnosis.append("Flow restriction")
            evidence.append(
                "Low flow rate indicates blockage or valve restriction."
            )

        if not diagnosis:
            diagnosis.append("System operating normally")

        confidence = 0.95 if safety.get("status") != "SAFE" else 0.90

        recommendations = []

        if "Pressure surge" in diagnosis:
            recommendations.append(
                "Inspect pressure relief valve."
            )

        if "Equipment overheating" in diagnosis:
            recommendations.append(
                "Check cooling system."
            )

        if "Possible gas leak" in diagnosis:
            recommendations.append(
                "Inspect pipelines and gas sensors."
            )

        if "Mechanical wear" in diagnosis:
            recommendations.append(
                "Inspect rotating equipment."
            )

        if "Flow restriction" in diagnosis:
            recommendations.append(
                "Inspect valves and pipelines."
            )

        if not recommendations:
            recommendations.append(
                "Continue monitoring."
            )

        metadata = {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "evidence": evidence,
            "source": "DiagnosticAgent",
        }

        self._store_metadata(
            context,
            metadata,
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=", ".join(diagnosis),
            confidence=confidence,
            evidence=evidence,
            recommendations=recommendations,
            required_action=(
                "Maintenance inspection"
                if diagnosis != ["System operating normally"]
                else "None"
            ),
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

    def _store_metadata(
        self,
        context,
        metadata,
    ):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["diagnosis"] = metadata

            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["diagnosis"] = metadata