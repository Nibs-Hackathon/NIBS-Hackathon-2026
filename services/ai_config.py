"""AI Configuration Generator - Runs once on startup to generate all thresholds and rules."""

import json
import re
import time
from typing import Dict, List, Any
from services.llm import LLMManager


class AIConfigGenerator:
    """Generate all configuration using AI once at startup."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if AIConfigGenerator._config is None:
            self.llm = LLMManager()
            self._generate_all_config()
    
    def _generate_all_config(self):
        """Generate ALL configuration in ONE AI call."""
        print("\n" + "="*60)
        print("🤖 AI CONFIGURATION GENERATOR")
        print("="*60)
        print("Generating all thresholds and rules...")
        
        prompt = self._build_prompt()
        
        try:
            response = self.llm.generate(prompt, use_cache=True)
            config = self._parse_response(response)
            AIConfigGenerator._config = config
            self._save_to_file(config)
            print("✅ AI configuration generated successfully!")
        except Exception as e:
            print(f"⚠️ AI config generation failed: {e}")
            AIConfigGenerator._config = self._get_default_config()
            print("✅ Using default configuration as fallback")
        
        print("="*60 + "\n")
    
    def _build_prompt(self) -> str:
        """Build the comprehensive AI prompt."""
        return """
You are an industrial operations configuration expert. Generate a complete operational configuration for a refinery.

Return ONLY a JSON object with the following structure:

{
    "asset_types": {
        "Pump": {
            "thresholds": {
                "pressure_max": 150,
                "temperature_max": 85,
                "gas_max": 40,
                "vibration_max": 8,
                "flow_min": 25
            },
            "weight": {
                "pressure_weight": 30,
                "temperature_weight": 25,
                "gas_weight": 35,
                "vibration_weight": 20,
                "flow_weight": 10
            },
            "degradation_rate": 0.5,
            "critical_health": 50
        },
        "Compressor": {
            "thresholds": {
                "pressure_max": 160,
                "temperature_max": 90,
                "gas_max": 35,
                "vibration_max": 10,
                "flow_min": 30
            },
            "weight": {
                "pressure_weight": 35,
                "temperature_weight": 20,
                "gas_weight": 25,
                "vibration_weight": 30,
                "flow_weight": 10
            },
            "degradation_rate": 0.6,
            "critical_health": 50
        }
    },
    "workflow_sequences": {
        "pressure_spike": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
        "gas_leak": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
        "high_temperature": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
        "high_vibration": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
        "flow_restriction": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]
    },
    "severity_mapping": {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    },
    "health_status_mapping": {
        "healthy": 80,
        "warning": 50,
        "critical": 30
    },
    "prediction": {
        "confidence_weight": 0.55,
        "sample_weight": 0.02,
        "max_samples": 20,
        "rul_max_days": 365,
        "rul_min_days": 1
    },
    "notification": {
        "critical_failure_threshold": 70,
        "warning_failure_threshold": 40,
        "info_failure_threshold": 0
    }
}

Generate for ALL asset types: Pump, Compressor, Tank, Valve, Pipeline, Heat Exchanger, Reactor, Boiler, Turbine, Motor, Generator, Distillation Column.

Use realistic industrial values. Respond with ONLY valid JSON, no other text.
"""
    
    def _parse_response(self, response: str) -> Dict:
        """Parse JSON from AI response."""
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            json_str = response[start:end]
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            return json.loads(json_str)
        raise ValueError("No JSON found in response")
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "asset_types": {
                "Pump": {
                    "thresholds": {"pressure_max": 150, "temperature_max": 85, "gas_max": 40, "vibration_max": 8, "flow_min": 25},
                    "weight": {"pressure_weight": 30, "temperature_weight": 25, "gas_weight": 35, "vibration_weight": 20, "flow_weight": 10},
                    "degradation_rate": 0.5,
                    "critical_health": 50
                },
                "Compressor": {
                    "thresholds": {"pressure_max": 160, "temperature_max": 90, "gas_max": 35, "vibration_max": 10, "flow_min": 30},
                    "weight": {"pressure_weight": 35, "temperature_weight": 20, "gas_weight": 25, "vibration_weight": 30, "flow_weight": 10},
                    "degradation_rate": 0.6,
                    "critical_health": 50
                },
                "Tank": {
                    "thresholds": {"pressure_max": 120, "temperature_max": 80, "gas_max": 45, "vibration_max": 5, "flow_min": 20},
                    "weight": {"pressure_weight": 20, "temperature_weight": 30, "gas_weight": 40, "vibration_weight": 10, "flow_weight": 10},
                    "degradation_rate": 0.3,
                    "critical_health": 50
                },
                "Valve": {
                    "thresholds": {"pressure_max": 140, "temperature_max": 85, "gas_max": 40, "vibration_max": 7, "flow_min": 15},
                    "weight": {"pressure_weight": 25, "temperature_weight": 25, "gas_weight": 30, "vibration_weight": 20, "flow_weight": 15},
                    "degradation_rate": 0.4,
                    "critical_health": 50
                },
                "Pipeline": {
                    "thresholds": {"pressure_max": 130, "temperature_max": 80, "gas_max": 50, "vibration_max": 6, "flow_min": 10},
                    "weight": {"pressure_weight": 30, "temperature_weight": 15, "gas_weight": 45, "vibration_weight": 10, "flow_weight": 10},
                    "degradation_rate": 0.3,
                    "critical_health": 50
                },
                "Heat Exchanger": {
                    "thresholds": {"pressure_max": 145, "temperature_max": 100, "gas_max": 30, "vibration_max": 9, "flow_min": 25},
                    "weight": {"pressure_weight": 20, "temperature_weight": 35, "gas_weight": 20, "vibration_weight": 25, "flow_weight": 15},
                    "degradation_rate": 0.7,
                    "critical_health": 50
                },
                "Reactor": {
                    "thresholds": {"pressure_max": 155, "temperature_max": 95, "gas_max": 35, "vibration_max": 8, "flow_min": 20},
                    "weight": {"pressure_weight": 30, "temperature_weight": 25, "gas_weight": 25, "vibration_weight": 20, "flow_weight": 10},
                    "degradation_rate": 0.5,
                    "critical_health": 50
                },
                "Boiler": {
                    "thresholds": {"pressure_max": 170, "temperature_max": 120, "gas_max": 25, "vibration_max": 10, "flow_min": 30},
                    "weight": {"pressure_weight": 35, "temperature_weight": 30, "gas_weight": 15, "vibration_weight": 20, "flow_weight": 10},
                    "degradation_rate": 0.8,
                    "critical_health": 50
                },
                "Turbine": {
                    "thresholds": {"pressure_max": 140, "temperature_max": 100, "gas_max": 30, "vibration_max": 12, "flow_min": 25},
                    "weight": {"pressure_weight": 25, "temperature_weight": 20, "gas_weight": 20, "vibration_weight": 35, "flow_weight": 10},
                    "degradation_rate": 0.6,
                    "critical_health": 50
                },
                "Motor": {
                    "thresholds": {"pressure_max": 120, "temperature_max": 95, "gas_max": 30, "vibration_max": 15, "flow_min": 20},
                    "weight": {"pressure_weight": 15, "temperature_weight": 25, "gas_weight": 15, "vibration_weight": 45, "flow_weight": 10},
                    "degradation_rate": 0.5,
                    "critical_health": 50
                },
                "Generator": {
                    "thresholds": {"pressure_max": 130, "temperature_max": 100, "gas_max": 25, "vibration_max": 14, "flow_min": 25},
                    "weight": {"pressure_weight": 20, "temperature_weight": 30, "gas_weight": 15, "vibration_weight": 35, "flow_weight": 10},
                    "degradation_rate": 0.5,
                    "critical_health": 50
                },
                "Distillation Column": {
                    "thresholds": {"pressure_max": 125, "temperature_max": 110, "gas_max": 30, "vibration_max": 7, "flow_min": 15},
                    "weight": {"pressure_weight": 25, "temperature_weight": 35, "gas_weight": 25, "vibration_weight": 15, "flow_weight": 10},
                    "degradation_rate": 0.4,
                    "critical_health": 50
                }
            },
            "workflow_sequences": {
                "pressure_spike": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
                "gas_leak": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
                "high_temperature": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
                "high_vibration": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
                "flow_restriction": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]
            },
            "severity_mapping": {"Critical": 1, "High": 2, "Medium": 3, "Low": 4},
            "health_status_mapping": {"healthy": 80, "warning": 50, "critical": 30},
            "prediction": {"confidence_weight": 0.55, "sample_weight": 0.02, "max_samples": 20, "rul_max_days": 365, "rul_min_days": 1},
            "notification": {"critical_failure_threshold": 70, "warning_failure_threshold": 40, "info_failure_threshold": 0}
        }
    
    def _save_to_file(self, config: Dict):
        """Save config to file for cache."""
        try:
            import json
            from pathlib import Path
            config_path = Path(__file__).resolve().parents[1] / "data" / "ai_config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Config saved to {config_path}")
        except Exception as e:
            print(f"⚠️ Could not save config: {e}")
    
    def get_config(self) -> Dict:
        """Get the generated configuration."""
        return AIConfigGenerator._config or self._get_default_config()
    
    def get_asset_config(self, asset_type: str) -> Dict:
        """Get config for a specific asset type."""
        config = self.get_config()
        return config.get("asset_types", {}).get(asset_type, config.get("asset_types", {}).get("Pump", {}))
    
    def get_thresholds(self, asset_type: str) -> Dict:
        """Get thresholds for a specific asset type."""
        asset_config = self.get_asset_config(asset_type)
        return asset_config.get("thresholds", {})
    
    def get_workflow_sequence(self, incident_type: str) -> List[str]:
        """Get workflow sequence for an incident type."""
        config = self.get_config()
        return config.get("workflow_sequences", {}).get(incident_type, ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"])
    
    def get_prediction_params(self) -> Dict:
        """Get prediction parameters."""
        config = self.get_config()
        return config.get("prediction", {})
    
    def get_severity_priority(self, severity: str) -> int:
        """Get priority for a severity level."""
        config = self.get_config()
        return config.get("severity_mapping", {}).get(severity, 3)