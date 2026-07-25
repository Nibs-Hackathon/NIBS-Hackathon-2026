"""
mao/workflows/planner.py

Workflow Planner

Determines which workflow should execute based on the
incoming event and telemetry payload.

Supports both:
    • Explicit event names
    • Automatic telemetry-based routing
"""

from __future__ import annotations

from typing import Any


class Planner:
    """
    Selects the most appropriate workflow for an incoming event.
    """

    EVENT_MAP = {
        "PressureSpike": "pressure_response",
        "HighTemperature": "temperature_response",
        "GasLeak": "gas_response",
        "HighVibration": "maintenance_response",
        "FlowRestriction": "flow_response",
    }

    def choose_workflow(self, event: Any) -> str:
        """
        Determine which workflow should handle an event.

        Priority:
            1. Telemetry inspection
            2. Event-name lookup
            3. Default workflow
        """

        payload = getattr(event, "payload", {}) or {}

        workflow = self._workflow_from_payload(payload)

        if workflow is not None:
            return workflow

        return self.EVENT_MAP.get(
            getattr(event, "name", ""),
            "default",
        )

    def _workflow_from_payload(
        self,
        payload: dict,
    ) -> str | None:
        """
        Infer workflow directly from telemetry.
        """

        pressure = payload.get("pressure")
        temperature = payload.get("temperature")
        gas = payload.get("gas_level")
        vibration = payload.get("vibration")
        flow = payload.get("flow_rate")

        if pressure is not None and pressure >= 150:
            return "pressure_response"

        if temperature is not None and temperature >= 85:
            return "temperature_response"

        if gas is not None and gas >= 40:
            return "gas_response"

        if vibration is not None and vibration >= 8:
            return "maintenance_response"

        if flow is not None and flow <= 25:
            return "flow_response"

        return None