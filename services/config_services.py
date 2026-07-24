"""Gemini-powered dynamic configuration service."""

import json
import re
from typing import Any, Dict, List, Optional
from services.llm import LLMManager


class ConfigService:
    """Generate and cache operational configurations using Gemini."""

    _instance = None
    _cache: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.llm = LLMManager()

    def get_thresholds(self, asset_type: str, context: Optional[str] = None) -> Dict[str, float]:
        """Generate asset-specific thresholds using Gemini."""
        cache_key = f"thresholds_{asset_type}_{context or 'default'}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = f"""
You are an industrial operations configuration expert.

Generate operational thresholds for a {asset_type} asset in a {context or 'standard'} industrial environment.

Return ONLY a JSON object with these fields:
- pressure_max: float (maximum safe pressure in PSI)
- temperature_max: float (maximum safe temperature in °C)
- gas_max: float (maximum safe gas concentration in ppm)
- vibration_max: float (maximum safe vibration in mm/s)
- flow_min: float (minimum safe flow rate in L/min)

Use realistic values for {asset_type} equipment.
Respond with ONLY valid JSON, no other text.
"""

        try:
            response = self.llm.generate(prompt)
            thresholds = self._parse_json(response)
            self._cache[cache_key] = thresholds
            return thresholds
        except Exception as e:
            print(f"⚠️ Gemini config generation failed: {e}")
            return self._get_default_thresholds(asset_type)

    def _parse_json(self, response: str) -> Dict:
        """Extract JSON from Gemini response."""
        # Find JSON-like content
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            json_str = response[start:end]
            # Clean up common issues
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            return json.loads(json_str)
        raise ValueError("No JSON found in response")

    def _get_default_thresholds(self, asset_type: str) -> Dict:
        """Fallback thresholds when Gemini is unavailable."""
        defaults = {
            "Pump": {"pressure_max": 150, "temperature_max": 85, "gas_max": 40, "vibration_max": 8, "flow_min": 25},
            "Compressor": {"pressure_max": 160, "temperature_max": 90, "gas_max": 35, "vibration_max": 10, "flow_min": 30},
            "Tank": {"pressure_max": 120, "temperature_max": 80, "gas_max": 45, "vibration_max": 5, "flow_min": 20},
            "Valve": {"pressure_max": 140, "temperature_max": 85, "gas_max": 40, "vibration_max": 7, "flow_min": 15},
            "Pipeline": {"pressure_max": 130, "temperature_max": 80, "gas_max": 50, "vibration_max": 6, "flow_min": 10},
            "Heat Exchanger": {"pressure_max": 145, "temperature_max": 100, "gas_max": 30, "vibration_max": 9, "flow_min": 25},
        }
        return defaults.get(asset_type, defaults["Pump"])

    def get_workflow_sequence(self, incident_type: str) -> List[str]:
        """Generate agent sequence for an incident type."""
        cache_key = f"workflow_{incident_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = f"""
For an industrial {incident_type} incident, list the agents that should respond in order.

Available agents: sensor, safety, diagnostic, knowledge, maintenance, planning, prediction, notification, report

Return ONLY a JSON array of agent names.
Example: ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]
"""

        try:
            response = self.llm.generate(prompt)
            sequence = self._parse_json(response)
            if isinstance(sequence, list):
                self._cache[cache_key] = sequence
                return sequence
        except Exception:
            pass

        # Fallback - standard sequence
        return ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]

    def get_priority_level(self, incident_type: str, severity: str) -> int:
        """Generate priority level for an incident."""
        prompt = f"""
For an industrial {incident_type} incident with {severity} severity, assign a priority level.

Priority is 1 (highest) to 9 (lowest).
Return ONLY an integer.
"""

        try:
            response = self.llm.generate(prompt)
            numbers = re.findall(r'\d+', response)
            if numbers:
                priority = int(numbers[0])
                return max(1, min(9, priority))
        except Exception:
            pass

        # Fallback
        severity_map = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
        return severity_map.get(severity, 3)

    def get_risk_weights(self, incident_type: str) -> Dict[str, int]:
        """Generate risk weights for different sensors."""
        cache_key = f"risk_weights_{incident_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = f"""
For a {incident_type} incident, assign risk weights (0-100) to each sensor type.

Return ONLY a JSON object with:
- pressure_weight: int
- temperature_weight: int
- gas_weight: int
- vibration_weight: int
- flow_weight: int

Sum of all weights should be 100.
"""

        try:
            response = self.llm.generate(prompt)
            weights = self._parse_json(response)
            self._cache[cache_key] = weights
            return weights
        except Exception:
            pass

        # Fallback
        return {"pressure_weight": 30, "temperature_weight": 25, "gas_weight": 35, "vibration_weight": 20, "flow_weight": 10}

    def clear_cache(self):
        """Clear the configuration cache."""
        self._cache = {}
        print("✅ Config cache cleared")

    def refresh(self):
        """Refresh all configurations by clearing cache."""
        self.clear_cache()
        return {"status": "refreshed", "cache_size": 0}