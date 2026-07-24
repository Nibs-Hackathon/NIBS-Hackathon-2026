# Folder: services Code Inventory

Generated: 2026-07-24 12:23:53 UTC

Contains 24 project files.

## services/__init__.py

**File path:** `services/__init__.py`

```python
"""Services module exports - NO circular imports."""

# ✅ Lazy imports to avoid circular issues
def get_asset_service():
    from services.asset import AssetService
    return AssetService

def get_health_service():
    from services.health import HealthService
    return HealthService

def get_llm_manager():
    from services.llm import LLMManager
    return LLMManager

def get_persistence_service():
    from services.persistence import PersistenceService
    return PersistenceService

def get_config_service():
    from services.config_services import ConfigService
    return ConfigService

def get_simulator_controller():
    from services.simulator_controller import SimulatorController, sim_controller
    return SimulatorController, sim_controller

def get_runtime():
    from services.runtime import kernel, simulator
    return kernel, simulator

def get_ai_config():
    """Get the AI Configuration Generator (singleton)."""
    from services.ai_config import AIConfigGenerator
    return AIConfigGenerator()

def get_computation_engine():
    """Get the Computation Engine (singleton)."""
    from services.computation_engine import ComputationEngine
    return ComputationEngine()


# Direct imports (safe ones)
from services.asset import AssetService
from services.health import HealthService
from services.llm import LLMManager
from services.persistence import PersistenceService
from services.config_services import ConfigService
from services.simulator_controller import SimulatorController, sim_controller
from services.runtime import kernel, simulator
from services.ai_config import AIConfigGenerator
from services.computation_engine import ComputationEngine

__all__ = [
    "AssetService",
    "HealthService",
    "LLMManager",
    "PersistenceService",
    "ConfigService",
    "SimulatorController",
    "sim_controller",
    "kernel",
    "simulator",
    "AIConfigGenerator",
    "ComputationEngine",
    "get_ai_config",
    "get_computation_engine",
]
```

## services/ai_config.py

**File path:** `services/ai_config.py`

```python
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
```

## services/asset.py

**File path:** `services/asset.py`

```python
from models.asset import Asset


class AssetService:

    def __init__(self):

        self.assets = {}

    def register(self, asset: Asset):

        self.assets[asset.id] = asset

    def get(self, asset_id):

        return self.assets.get(asset_id)

    def all_assets(self):

        return list(self.assets.values())

    def update_health(self, asset_id, health):

        asset = self.get(asset_id)

        if asset:
            asset.health = health

    def update_status(self, asset_id, status):

        asset = self.get(asset_id)

        if asset:
            asset.status = status

    
```

## services/computation_engine.py

**File path:** `services/computation_engine.py`

```python
"""Real-time computation engine - Runs every 10-15 seconds."""

import time
import math
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import deque
from services.ai_config import AIConfigGenerator
from models.sensor import SensorType


class ComputationEngine:
    """Computes health, failure probability, RUL in real-time."""
    
    _instance = None
    _last_computation = 0
    _computation_interval = 10  # seconds
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.config = AIConfigGenerator()
        self._history_cache: Dict[str, deque] = {}
        self._health_cache: Dict[str, float] = {}
        self._failure_cache: Dict[str, float] = {}
        self._rul_cache: Dict[str, float] = {}
        self._last_tick = 0
    
    def should_compute(self, tick: int) -> bool:
        """Check if computation should run (every 10-15 seconds)."""
        now = time.time()
        if now - self._last_computation >= self._computation_interval:
            self._last_computation = now
            return True
        return False
    
    def compute_all(self, tick: int, telemetry: List[Any], assets: List[Any]) -> Dict:
        """Compute everything for all assets."""
        if not self.should_compute(tick):
            return self._get_cached_results()
        
        print(f"🧮 Computing health metrics at tick {tick}...")
        start = time.time()
        
        results = {}
        for asset in assets:
            asset_telemetry = [t for t in telemetry if t.asset_id == asset.id]
            result = self.compute_asset(asset, asset_telemetry)
            results[asset.id] = result
        
        elapsed = time.time() - start
        print(f"✅ Computation completed in {elapsed:.3f}s for {len(assets)} assets")
        
        return results
    
    def compute_asset(self, asset: Any, telemetry: List[Any]) -> Dict:
        """Compute metrics for a single asset."""
        if not telemetry:
            return {
                "health": 100.0,
                "failure_probability": 0.0,
                "rul_days": 365,
                "confidence": 0.0,
                "status": "Running",
                "degradation_rate": 0.0,
            }
        
        # Get asset type config
        asset_type = asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type)
        config = self.config.get_asset_config(asset_type)
        thresholds = config.get("thresholds", {})
        weights = config.get("weight", {})
        degradation_rate_base = config.get("degradation_rate", 0.5)
        critical_health = config.get("critical_health", 50)
        
        # 1. Calculate health
        health = self._calculate_health(telemetry, thresholds, weights)
        
        # 2. Calculate degradation rate
        degradation_rate = self._calculate_degradation_rate(telemetry, degradation_rate_base)
        
        # 3. Calculate failure probability
        failure_probability = self._calculate_failure_probability(health, degradation_rate)
        
        # 4. Calculate RUL
        rul_days = self._calculate_rul(health, degradation_rate)
        
        # 5. Calculate confidence
        confidence = self._calculate_confidence(len(telemetry))
        
        # 6. Determine status
        status = self._determine_status(health, critical_health)
        
        return {
            "health": round(health, 1),
            "failure_probability": round(failure_probability, 1),
            "rul_days": round(rul_days, 1),
            "confidence": round(confidence, 2),
            "status": status,
            "degradation_rate": round(degradation_rate, 3),
            "telemetry_count": len(telemetry),
            "asset_type": asset_type,
        }
    
    def _calculate_health(self, telemetry: List[Any], thresholds: Dict, weights: Dict) -> float:
        """Calculate health based on telemetry violations."""
        health = 100.0
        violations = {}
        
        for reading in telemetry:
            sensor_type = reading.sensor_type
            
            # Check each sensor against thresholds
            if sensor_type == SensorType.PRESSURE:
                limit = thresholds.get("pressure_max", 150)
                if reading.value > limit:
                    violation = (reading.value - limit) / limit * 100
                    violations["pressure"] = max(violations.get("pressure", 0), violation)
            
            elif sensor_type == SensorType.TEMPERATURE:
                limit = thresholds.get("temperature_max", 85)
                if reading.value > limit:
                    violation = (reading.value - limit) / limit * 100
                    violations["temperature"] = max(violations.get("temperature", 0), violation)
            
            elif sensor_type == SensorType.GAS:
                limit = thresholds.get("gas_max", 40)
                if reading.value > limit:
                    violation = (reading.value - limit) / limit * 100
                    violations["gas"] = max(violations.get("gas", 0), violation)
            
            elif sensor_type == SensorType.VIBRATION:
                limit = thresholds.get("vibration_max", 8)
                if reading.value > limit:
                    violation = (reading.value - limit) / limit * 100
                    violations["vibration"] = max(violations.get("vibration", 0), violation)
            
            elif sensor_type == SensorType.FLOW:
                limit = thresholds.get("flow_min", 25)
                if reading.value < limit:
                    violation = (limit - reading.value) / limit * 100
                    violations["flow"] = max(violations.get("flow", 0), violation)
        
        # Apply weighted violations
        total_weight = 0
        weighted_violation = 0
        
        for sensor, violation in violations.items():
            weight = weights.get(f"{sensor}_weight", 20)
            total_weight += weight
            weighted_violation += violation * (weight / 100)
        
        # Reduce health based on violations
        if total_weight > 0:
            health = max(0, health - weighted_violation)
        
        # Apply degradation over time (exponential decay)
        # Each telemetry point adds slight degradation
        degradation_factor = min(1, len(telemetry) / 1000)
        health = health * (1 - 0.001 * degradation_factor)
        
        return max(0, min(100, health))
    
    def _calculate_degradation_rate(self, telemetry: List[Any], base_rate: float) -> float:
        """Calculate degradation rate from telemetry trends."""
        if len(telemetry) < 2:
            return base_rate
        
        # Calculate trend
        values = []
        for reading in telemetry:
            if reading.sensor_type == SensorType.VIBRATION:
                values.append(reading.value)
            elif reading.sensor_type == SensorType.TEMPERATURE:
                values.append(reading.value * 0.5)  # Weight temperature less
        
        if len(values) < 2:
            return base_rate
        
        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        # Convert slope to degradation rate (0.1 to 2.0)
        rate = abs(slope) * 0.1
        
        # Scale to reasonable range
        degradation_rate = max(0.1, min(2.0, rate + base_rate * 0.5))
        
        return degradation_rate
    
    def _calculate_failure_probability(self, health: float, degradation_rate: float) -> float:
        """Calculate failure probability from health and degradation."""
        # Base probability from health
        health_factor = (100 - health) / 100  # 0-1
        
        # Degradation factor
        degradation_factor = min(1, degradation_rate / 1.0)
        
        # Combined probability
        probability = health_factor * 0.7 + degradation_factor * 0.3
        
        # Exponential scaling
        probability = 1 - math.exp(-probability * 3)
        
        return min(100, max(0, probability * 100))
    
    def _calculate_rul(self, health: float, degradation_rate: float) -> float:
        """Calculate Remaining Useful Life in days."""
        if degradation_rate <= 0:
            return 365
        
        # Time to reach 0 health
        rul = health / (degradation_rate * 5)  # Scale factor
        
        return max(1, min(365, rul))
    
    def _calculate_confidence(self, sample_count: int) -> float:
        """Calculate confidence based on sample count."""
        confidence = 0.55 + min(sample_count, 20) * 0.02
        return min(0.95, confidence)
    
    def _determine_status(self, health: float, critical_health: float) -> str:
        """Determine status from health value."""
        if health >= 80:
            return "Running"
        elif health >= critical_health:
            return "Warning"
        elif health >= 30:
            return "Critical"
        else:
            return "Offline"
    
    def _get_cached_results(self) -> Dict:
        """Return cached results if computation not needed."""
        return {}
    
    def get_asset_health(self, asset_id: str) -> Optional[float]:
        """Get cached health for an asset."""
        return self._health_cache.get(asset_id)
    
    def get_asset_failure_probability(self, asset_id: str) -> Optional[float]:
        """Get cached failure probability for an asset."""
        return self._failure_cache.get(asset_id)
    
    def get_asset_rul(self, asset_id: str) -> Optional[float]:
        """Get cached RUL for an asset."""
        return self._rul_cache.get(asset_id)
```

## services/config_services.py

**File path:** `services/config_services.py`

```python
"""Optimized Gemini-powered dynamic configuration service with precomputation."""

import json
import re
import time
from typing import Any, Dict, List, Optional
from functools import lru_cache
from services.llm import LLMManager


class ConfigService:
    """Generate and cache operational configurations using Gemini."""

    _instance = None
    _cache: Dict[str, Any] = {}
    _precomputed: Dict[str, Any] = {}
    _precomputed_done = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.llm = LLMManager()
        if not ConfigService._precomputed_done:
            self._precompute_defaults()
            ConfigService._precomputed_done = True

    def _precompute_defaults(self):
        """Precompute common configurations for all asset types."""
        asset_types = ["Pump", "Compressor", "Tank", "Valve", "Pipeline", "Heat Exchanger", "Reactor", "Boiler", "Turbine"]
        
        for asset_type in asset_types:
            cache_key = f"thresholds_{asset_type}_default"
            if cache_key not in self._precomputed:
                try:
                    self._precomputed[cache_key] = self._generate_thresholds(asset_type)
                except:
                    self._precomputed[cache_key] = self._get_default_thresholds(asset_type)
        
        print(f"✅ Precomputed thresholds for {len(asset_types)} asset types")

    @lru_cache(maxsize=128)
    def _generate_thresholds(self, asset_type: str) -> Dict[str, float]:
        """Generate thresholds with caching."""
        prompt = f"""
You are an industrial operations configuration expert.

Generate operational thresholds for a {asset_type} asset.

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
            response = self.llm.generate(prompt, use_cache=True)
            return self._parse_json(response)
        except Exception as e:
            print(f"⚠️ Gemini config generation failed: {e}")
            return self._get_default_thresholds(asset_type)

    def _parse_json(self, response: str) -> Dict:
        """Extract JSON from Gemini response."""
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            json_str = response[start:end]
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
            "Reactor": {"pressure_max": 155, "temperature_max": 95, "gas_max": 35, "vibration_max": 8, "flow_min": 20},
            "Boiler": {"pressure_max": 170, "temperature_max": 120, "gas_max": 25, "vibration_max": 10, "flow_min": 30},
            "Turbine": {"pressure_max": 140, "temperature_max": 100, "gas_max": 30, "vibration_max": 12, "flow_min": 25},
        }
        return defaults.get(asset_type, defaults["Pump"])

    def get_thresholds(self, asset_type: str, context: Optional[str] = None) -> Dict[str, float]:
        """Get thresholds - uses precomputed values for speed."""
        # ✅ Check precomputed first (super fast)
        precomputed_key = f"thresholds_{asset_type}_default"
        if precomputed_key in self._precomputed:
            return self._precomputed[precomputed_key]
        
        cache_key = f"thresholds_{asset_type}_{context or 'default'}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        thresholds = self._generate_thresholds(asset_type)
        self._cache[cache_key] = thresholds
        return thresholds

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
            response = self.llm.generate(prompt, use_cache=True)
            sequence = self._parse_json(response)
            if isinstance(sequence, list):
                self._cache[cache_key] = sequence
                return sequence
        except Exception:
            pass

        return ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]

    def get_priority_level(self, incident_type: str, severity: str) -> int:
        """Generate priority level for an incident."""
        prompt = f"""
For an industrial {incident_type} incident with {severity} severity, assign a priority level.

Priority is 1 (highest) to 9 (lowest).
Return ONLY an integer.
"""

        try:
            response = self.llm.generate(prompt, use_cache=True)
            numbers = re.findall(r'\d+', response)
            if numbers:
                priority = int(numbers[0])
                return max(1, min(9, priority))
        except Exception:
            pass

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
            response = self.llm.generate(prompt, use_cache=True)
            weights = self._parse_json(response)
            self._cache[cache_key] = weights
            return weights
        except Exception:
            pass

        return {"pressure_weight": 30, "temperature_weight": 25, "gas_weight": 35, "vibration_weight": 20, "flow_weight": 10}

    def clear_cache(self):
        """Clear the configuration cache."""
        self._cache = {}
        print("✅ Config cache cleared")

    def refresh(self):
        """Refresh all configurations by clearing cache."""
        self.clear_cache()
        return {"status": "refreshed", "cache_size": 0}
```

## services/embedding.py

**File path:** `services/embedding.py`

```python

```

## services/health.py

**File path:** `services/health.py`

```python
"""Health service using the computation engine with AI-generated thresholds."""

from models.sensor import SensorType
from services.computation_engine import ComputationEngine


class HealthService:
    """
    Calculates asset health from recent telemetry using AI-generated thresholds.
    """

    def __init__(self):
        self.engine = ComputationEngine()
        self._threshold_cache = {}

    def calculate_health(self, readings):
        """
        Calculate health from readings using AI-generated thresholds.
        
        Args:
            readings: List of sensor readings for an asset
            
        Returns:
            float: Health score (0-100)
        """
        if not readings:
            return 100.0

        # Get asset type from first reading
        asset_id = readings[0].asset_id
        asset = self.engine.kernel.asset_service.get(asset_id)
        asset_type = asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type)
        
        # Get thresholds from AI config
        thresholds = self.engine.config.get_thresholds(asset_type)
        weights = self.engine.config.get_asset_config(asset_type).get("weight", {})
        
        # Calculate health using the engine
        health = self.engine._calculate_health(readings, thresholds, weights)
        
        return max(0.0, min(100.0, health))

    def calculate_health_with_limits(self, readings, limits=None):
        """
        Calculate health with custom limits (fallback method).
        
        Args:
            readings: List of sensor readings
            limits: Optional custom limits dict
            
        Returns:
            float: Health score (0-100)
        """
        if not readings:
            return 100.0

        if limits is None:
            limits = {
                SensorType.PRESSURE: 150,
                SensorType.TEMPERATURE: 90,
                SensorType.FLOW: 40,
                SensorType.VIBRATION: 25,
                SensorType.GAS: 15,
            }

        health = 100.0

        for reading in readings:
            limit = limits.get(reading.sensor_type)
            if limit is None:
                continue

            if reading.sensor_type == SensorType.FLOW:
                if reading.value < limit:
                    health -= 5
            else:
                if reading.value > limit:
                    health -= 5

        return max(0.0, health)

    def get_health_metrics(self, asset, telemetry):
        """
        Get full health metrics for an asset using computation engine.
        
        Args:
            asset: Asset object
            telemetry: List of telemetry readings
            
        Returns:
            dict: Full health metrics
        """
        return self.engine.compute_asset(asset, telemetry)

    def get_asset_health_status(self, asset_id):
        """
        Get cached health status for an asset.
        
        Args:
            asset_id: ID of the asset
            
        Returns:
            dict: Health status including health, status, failure probability
        """
        health = self.engine.get_asset_health(asset_id)
        failure_prob = self.engine.get_asset_failure_probability(asset_id)
        rul = self.engine.get_asset_rul(asset_id)
        
        if health is None:
            return {"health": 100, "status": "Running", "failure_probability": 0, "rul": "365 days"}
        
        return {
            "health": health,
            "status": self.engine._determine_status(health, 50),
            "failure_probability": failure_prob or 0,
            "rul": rul or 365
        }
```

## services/incident_manager.py

**File path:** `services/incident_manager.py`

```python
from datetime import datetime
from uuid import uuid4

from models.incident import Incident
from models.enums import IncidentSeverity


class IncidentManager:

    def __init__(self):

        self.active = {}
        self.history = []

    def create(self, event):

        incident = Incident(
            id=str(uuid4()),
            asset_id=event.source,
            title=event.name,
            description=str(event.payload),
            severity=IncidentSeverity.HIGH,
            detected_at=datetime.now(),
        )

        self.active[incident.id] = incident

        self.history.append(incident)

        return incident

    def resolve(self, incident_id):

        if incident_id in self.active:

            self.active[incident_id].resolved = True

            del self.active[incident_id]

    def list_active(self):

        return list(self.active.values())
```

## services/incident_service.py

**File path:** `services/incident_service.py`

```python
from models.sensor import SensorType
from services.kernel_factory import get_kernel

class IncidentService:

    def __init__(self, simulator):
        self.simulator = simulator


    def trigger_incident(self, incident_type):

        fault = None

        incident_type = incident_type.lower()


        if incident_type == "pressure spike":

            fault = {
                "sensor": SensorType.PRESSURE,
                "value": 155
            }


        elif incident_type == "gas leak":

            fault = {
                "sensor": SensorType.GAS,
                "value": 30
            }


        elif incident_type == "high vibration":

            fault = {
                "sensor": SensorType.VIBRATION,
                "value": 40
            }


        elif incident_type == "high temperature":

            fault = {
                "sensor": SensorType.TEMPERATURE,
                "value": 95
            }


        elif incident_type == "flow restriction":

            fault = {
                "sensor": SensorType.FLOW,
                "value": 15
            }


        telemetry, reports = self.simulator.tick(
            tick_number=1,
            fault=fault
        )


        return {
            "telemetry": telemetry,
            "reports": reports
        }
```

## services/kernel_factory.py

**File path:** `services/kernel_factory.py`

```python
"""
services/kernel_factory.py

Compatibility access point for the shared MAO kernel.
"""

from mao import MAOKernel
from services.runtime import kernel


def create_kernel() -> MAOKernel:
    """
    Return the already initialized production kernel.
    """

    return kernel



def get_kernel() -> MAOKernel:
    """
    Return the shared MAO kernel instance.
    """

    return kernel
```

## services/llm.py

**File path:** `services/llm.py`

```python
"""Centralized, failover-safe access to Gemini models with multi-key rotation and caching."""

import hashlib
import logging
import os
import socket
import time
from pathlib import Path
from typing import Optional, Dict, List
from collections import deque
from datetime import datetime
from urllib.parse import urlsplit

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# ✅ SUPPORTED ENV VARS - ALL POSSIBLE NAMING CONVENTIONS
SUPPORTED_GEMINI_ENV_VARS = (
    # Standard naming
    "GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3",
    "GEMINI_API_KEY_4", "GEMINI_API_KEY_5", "GEMINI_API_KEY_6",
    "GEMINI_API_KEY_7", "GEMINI_API_KEY_8", "GEMINI_API_KEY_9",
    "GEMINI_API_KEY_10",
    # Alternative naming
    "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3",
    "GOOGLE_API_KEY_4", "GOOGLE_API_KEY_5", "GOOGLE_API_KEY_6",
    "GOOGLE_API_KEY_7",
    # Single key fallback
    "GEMINI_API_KEY", "GOOGLE_API_KEY",
)

DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"

_PROXY_ENV_VARS = (
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
    "http_proxy", "https_proxy", "all_proxy",
)
_LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _has_invalid_gemini_proxy() -> bool:
    """Return whether this process inherited the known dead loopback proxy."""
    for name in _PROXY_ENV_VARS:
        value = os.getenv(name)
        if not value:
            continue
        try:
            proxy = urlsplit(value)
            if proxy.hostname not in _LOOPBACK_HOSTS or proxy.port is None:
                continue
            if proxy.port == 9:
                return True
            with socket.create_connection((proxy.hostname, proxy.port), timeout=0.15):
                pass
        except OSError:
            return True
        except ValueError:
            continue
    return False


class RateLimiter:
    """Simple rate limiter for API calls with per-key tracking."""

    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.call_timestamps: Dict[str, deque] = {}

    def wait_if_needed(self, key: str):
        """Wait if rate limit would be exceeded for a specific key."""
        now = time.time()

        if key not in self.call_timestamps:
            self.call_timestamps[key] = deque(maxlen=self.calls_per_minute)

        timestamps = self.call_timestamps[key]

        while timestamps and now - timestamps[0] > 60:
            timestamps.popleft()

        if len(timestamps) >= self.calls_per_minute:
            oldest = timestamps[0]
            wait_time = 60 - (now - oldest) + 0.5
            if wait_time > 0:
                logger.warning(f"Rate limit reached for key, waiting {wait_time:.2f}s")
                time.sleep(wait_time)

        timestamps.append(time.time())


class KeyStatus:
    """Track status of each API key."""

    def __init__(self, key: str, index: int):
        self.key = key
        self.index = index
        self.failures = 0
        self.successes = 0
        self.last_used: Optional[float] = None
        self.last_error: Optional[str] = None
        self.is_active = True
        self.cooldown_until: Optional[float] = None
        self.total_requests = 0

    def record_success(self):
        self.successes += 1
        self.failures = 0
        self.last_used = time.time()
        self.total_requests += 1
        self.is_active = True

    def record_failure(self, error: str):
        self.failures += 1
        self.last_error = error
        self.total_requests += 1

        # ✅ More aggressive cooldown - 30 seconds instead of 60
        if self.failures >= 3:
            self.is_active = False
            self.cooldown_until = time.time() + 30
            logger.warning(f"Key {self.index + 1} deactivated for 30s due to {self.failures} failures")

    def reactivate_if_ready(self):
        if not self.is_active and self.cooldown_until:
            if time.time() >= self.cooldown_until:
                self.is_active = True
                self.failures = 0
                self.cooldown_until = None
                logger.info(f"Key {self.index + 1} reactivated after cooldown")
                return True
        return False

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.successes / self.total_requests) * 100

    @property
    def is_available(self) -> bool:
        if not self.is_active:
            return False
        if self.cooldown_until and time.time() < self.cooldown_until:
            return False
        return True

    def to_dict(self) -> Dict:
        return {
            "index": self.index + 1,
            "key_preview": self.key[:8] + "..." + self.key[-4:],
            "is_active": self.is_active,
            "is_available": self.is_available,
            "failures": self.failures,
            "successes": self.successes,
            "total_requests": self.total_requests,
            "success_rate": f"{self.success_rate:.1f}%",
            "last_used": datetime.fromtimestamp(self.last_used).strftime("%H:%M:%S") if self.last_used else "Never",
            "last_error": self.last_error or "None",
        }


# Response Cache
_response_cache: Dict[str, tuple] = {}
_CACHE_MAX_SIZE = 100


class LLMManager:
    """Central Gemini router with automatic multi-key rotation and caching."""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
        self.keys = self._load_keys()
        self.current_key_index = 0
        self.key_statuses: Dict[str, KeyStatus] = {}
        self.rate_limiter = RateLimiter(calls_per_minute=60)

        for idx, key in enumerate(self.keys):
            self.key_statuses[key] = KeyStatus(key, idx)

        if not self.keys:
            raise RuntimeError(
                "No Gemini API key was found. Configure one of:\n"
                + "\n".join(f"  - {var}" for var in SUPPORTED_GEMINI_ENV_VARS)
            )

        logger.info(f"LLMManager initialized with {len(self.keys)} Gemini key(s)")

    def _load_keys(self) -> List[str]:
        """✅ Load API keys from ALL possible sources."""
        keys = []
        seen = set()

        # 1. Check environment variables
        print("\n🔑 Loading Gemini API Keys...")
        for var in SUPPORTED_GEMINI_ENV_VARS:
            value = os.getenv(var)
            if value and value not in seen:
                seen.add(value)
                keys.append(value)
                print(f"  ✅ Loaded from {var}: {value[:8]}...{value[-4:]}")

        # 2. Check .env file directly
        try:
            env_path = PROJECT_ROOT / ".env"
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('GEMINI_API_KEY') or line.startswith('GOOGLE_API_KEY'):
                            if '=' in line:
                                key = line.split('=', 1)[1].strip()
                                if key and key not in seen:
                                    seen.add(key)
                                    keys.append(key)
                                    print(f"  ✅ Loaded from .env: {key[:8]}...{key[-4:]}")
        except Exception as e:
            print(f"  ⚠️ Could not read .env: {e}")

        # 3. Check Streamlit secrets
        try:
            import streamlit as st
            for var in SUPPORTED_GEMINI_ENV_VARS:
                if var in st.secrets:
                    value = st.secrets[var]
                    if value and value not in seen:
                        seen.add(value)
                        keys.append(value)
                        print(f"  ✅ Loaded from secrets[{var}]: {value[:8]}...{value[-4:]}")
        except Exception:
            pass

        print(f"\n✅ Total keys loaded: {len(keys)}\n")
        return keys

    def _get_next_available_key(self) -> Optional[str]:
        """✅ Get the next available API key with rotation."""
        total_keys = len(self.keys)
        attempts = 0

        # Try all keys in rotation
        while attempts < total_keys:
            idx = self.current_key_index
            key = self.keys[idx]
            self.current_key_index = (self.current_key_index + 1) % total_keys

            status = self.key_statuses[key]
            
            # Try to reactivate if cooldown expired
            if not status.is_active:
                status.reactivate_if_ready()

            if status.is_available:
                status.last_used = time.time()
                return key

            attempts += 1

        # If all keys are exhausted, try to reactivate one
        for key in self.keys:
            status = self.key_statuses[key]
            if status.reactivate_if_ready():
                return key

        # Last resort: use first key (even if it's failing)
        return self.keys[0]

    def _create_model(self, key: str):
        """Create a Gemini model instance."""
        client_args = {"trust_env": False} if _has_invalid_gemini_proxy() else None
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=key,
            client_args=client_args,
            temperature=0.3,
        )

    def generate(self, prompt: str, max_retries_per_key: int = 2, use_cache: bool = True) -> str:
        """✅ Generate Gemini response with automatic multi-key rotation."""
        
        # Check cache first
        if use_cache:
            cache_key = hashlib.md5(prompt.encode()).hexdigest()
            if cache_key in _response_cache:
                cached_response, cached_time = _response_cache[cache_key]
                if time.time() - cached_time < 300:
                    logger.info(f"✅ Cache hit for prompt (key: {cache_key[:8]})")
                    return cached_response
                else:
                    del _response_cache[cache_key]
        
        last_error = None
        
        # ✅ Try each key in rotation
        for attempt in range(len(self.keys) * max_retries_per_key):
            try:
                key = self._get_next_available_key()
                if key is None:
                    raise RuntimeError("No available API keys")

                status = self.key_statuses[key]
                logger.info(f"Using Gemini key {status.index + 1}/{len(self.keys)}")

                self.rate_limiter.wait_if_needed(key)
                response = self._create_model(key).invoke(prompt)

                status.record_success()

                content = response.content
                if isinstance(content, str):
                    response_text = content
                elif isinstance(content, list):
                    response_text = "".join(
                        part if isinstance(part, str) else part.get("text", "")
                        for part in content
                        if isinstance(part, str) or isinstance(part, dict)
                    )
                else:
                    response_text = str(content)
                
                # Cache the response
                if use_cache and response_text:
                    cache_key = hashlib.md5(prompt.encode()).hexdigest()
                    _response_cache[cache_key] = (response_text, time.time())
                    
                    if len(_response_cache) > _CACHE_MAX_SIZE:
                        oldest_keys = sorted(_response_cache.keys(), key=lambda k: _response_cache[k][1])[:10]
                        for key in oldest_keys:
                            del _response_cache[key]
                
                return response_text

            except Exception as error:
                last_error = error
                error_str = str(error)
                
                # ✅ Handle rate limiting specially
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    logger.warning(f"⚠️ Key {status.index + 1} rate limited (429). Moving to next key.")
                    # ✅ Don't deactivate on rate limit - just use next key
                    if key and key in self.key_statuses:
                        status = self.key_statuses[key]
                        status.failures += 1
                        status.last_error = error_str
                    time.sleep(0.5)
                else:
                    if key and key in self.key_statuses:
                        status = self.key_statuses[key]
                        status.record_failure(error_str)
                        logger.warning(f"Key {status.index + 1} failed: {error_str[:100]}")
                    time.sleep(0.5)
                
                continue

        raise RuntimeError(
            f"All {len(self.keys)} Gemini API keys failed. Last error: {last_error}"
        ) from last_error

    def get_key_status(self) -> Dict[str, any]:
        """Get status of all API keys for monitoring."""
        return {
            "total_keys": len(self.keys),
            "model": self.model_name,
            "current_index": self.current_key_index + 1,
            "keys": [self.key_statuses[key].to_dict() for key in self.keys],
            "summary": {
                "active_keys": sum(1 for s in self.key_statuses.values() if s.is_active),
                "available_keys": sum(1 for s in self.key_statuses.values() if s.is_available),
                "total_requests": sum(s.total_requests for s in self.key_statuses.values()),
                "overall_success_rate": (
                    sum(s.successes for s in self.key_statuses.values()) /
                    max(1, sum(s.total_requests for s in self.key_statuses.values())) * 100
                ),
            }
        }

    def reset_key(self, key_index: int) -> bool:
        """Reset a specific key's status."""
        try:
            key = self.keys[key_index - 1]
            status = self.key_statuses[key]
            status.failures = 0
            status.is_active = True
            status.cooldown_until = None
            status.last_error = None
            logger.info(f"Key {key_index} reset successfully")
            return True
        except (IndexError, KeyError):
            return False

    def clear_cache(self):
        """Clear the response cache."""
        global _response_cache
        _response_cache.clear()
        logger.info("LLM response cache cleared")
```

## services/maintenance_scheduler.py

**File path:** `services/maintenance_scheduler.py`

```python
"""Maintenance scheduling service."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field


class MaintenancePriority(str, Enum):
    CRITICAL = "critical"   # Within 24 hours
    HIGH = "high"          # Within 3 days
    MEDIUM = "medium"      # Within 7 days
    LOW = "low"            # Within 30 days


@dataclass
class MaintenanceTask:
    """Maintenance task data."""
    id: str
    asset_id: str
    asset_name: str
    asset_type: str
    priority: MaintenancePriority
    description: str
    scheduled_date: datetime
    estimated_duration_hours: float
    estimated_cost: float
    assigned_team: str
    status: str = "scheduled"  # scheduled, in_progress, completed, cancelled
    created_at: datetime = field(default_factory=datetime.now)


class MaintenanceScheduler:
    """Schedule maintenance based on asset health and RUL."""
    
    _instance = None
    _tasks: List[MaintenanceTask] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def schedule_maintenance(self, asset: Dict, metrics: Dict) -> Optional[MaintenanceTask]:
        """Schedule maintenance for an asset based on its health."""
        health = metrics.get("health", 100)
        failure_probability = metrics.get("failure_probability", 0)
        rul_days = metrics.get("rul_days", 365)
        
        # Determine priority
        if failure_probability > 70 or rul_days < 7:
            priority = MaintenancePriority.CRITICAL
            scheduled_date = datetime.now() + timedelta(hours=12)
            duration = 6
        elif failure_probability > 40 or rul_days < 30:
            priority = MaintenancePriority.HIGH
            scheduled_date = datetime.now() + timedelta(days=1)
            duration = 4
        elif failure_probability > 20 or rul_days < 60:
            priority = MaintenancePriority.MEDIUM
            scheduled_date = datetime.now() + timedelta(days=3)
            duration = 2
        else:
            priority = MaintenancePriority.LOW
            scheduled_date = datetime.now() + timedelta(days=7)
            duration = 1
        
        # Check if already scheduled
        for task in self._tasks:
            if task.asset_id == asset.get("id") and task.status == "scheduled":
                return None
        
        # Estimate cost
        cost = self._estimate_cost(asset.get("type", "Pump"), duration, priority)
        
        task = MaintenanceTask(
            id=f"MT-{len(self._tasks) + 1:04d}",
            asset_id=asset.get("id", "unknown"),
            asset_name=asset.get("name", "Unknown Asset"),
            asset_type=asset.get("type", "Pump"),
            priority=priority,
            description=self._generate_description(asset, metrics),
            scheduled_date=scheduled_date,
            estimated_duration_hours=duration,
            estimated_cost=cost,
            assigned_team=self._assign_team(asset.get("type", "Pump")),
        )
        
        self._tasks.append(task)
        return task
    
    def _estimate_cost(self, asset_type: str, duration_hours: float, priority: MaintenancePriority) -> float:
        """Estimate maintenance cost."""
        base_costs = {
            "Pump": 500,
            "Compressor": 1000,
            "Tank": 300,
            "Valve": 200,
            "Pipeline": 800,
            "Heat Exchanger": 1200,
            "Reactor": 2000,
            "Boiler": 1500,
            "Turbine": 2500,
            "Motor": 400,
            "Generator": 1800,
            "Distillation Column": 3000,
        }
        
        base = base_costs.get(asset_type, 500)
        
        # Priority multiplier
        priority_multiplier = {
            MaintenancePriority.CRITICAL: 2.0,
            MaintenancePriority.HIGH: 1.5,
            MaintenancePriority.MEDIUM: 1.0,
            MaintenancePriority.LOW: 0.7,
        }
        
        return base * (duration_hours / 2) * priority_multiplier.get(priority, 1.0)
    
    def _assign_team(self, asset_type: str) -> str:
        """Assign maintenance team based on asset type."""
        team_map = {
            "Pump": "Rotating Equipment",
            "Compressor": "Rotating Equipment",
            "Tank": "Tank & Vessel",
            "Valve": "Instrumentation",
            "Pipeline": "Pipeline",
            "Heat Exchanger": "Utilities",
            "Reactor": "Process",
            "Boiler": "Utilities",
            "Turbine": "Rotating Equipment",
            "Motor": "Electrical",
            "Generator": "Electrical",
            "Distillation Column": "Process",
        }
        return team_map.get(asset_type, "General Maintenance")
    
    def _generate_description(self, asset: Dict, metrics: Dict) -> str:
        """Generate maintenance description."""
        health = metrics.get("health", 100)
        failure_prob = metrics.get("failure_probability", 0)
        
        if health < 40:
            return f"Emergency maintenance required - asset health at {health:.0f}%"
        elif health < 60:
            return f"Priority maintenance - asset health at {health:.0f}%, failure risk {failure_prob:.0f}%"
        elif health < 80:
            return f"Routine maintenance - asset health at {health:.0f}%, failure risk {failure_prob:.0f}%"
        else:
            return f"Preventive maintenance - asset health at {health:.0f}%"
    
    def get_upcoming_tasks(self, days: int = 7) -> List[MaintenanceTask]:
        """Get maintenance tasks scheduled in the next N days."""
        cutoff = datetime.now() + timedelta(days=days)
        return [t for t in self._tasks if t.scheduled_date <= cutoff and t.status == "scheduled"]
    
    def get_tasks_by_priority(self) -> Dict[MaintenancePriority, List[MaintenanceTask]]:
        """Get tasks grouped by priority."""
        result = {p: [] for p in MaintenancePriority}
        for task in self._tasks:
            if task.status == "scheduled":
                result[task.priority].append(task)
        return result
    
    def get_next_maintenance_date(self, asset_id: str) -> Optional[datetime]:
        """Get the next scheduled maintenance date for an asset."""
        tasks = [t for t in self._tasks if t.asset_id == asset_id and t.status == "scheduled"]
        if tasks:
            return min(t.scheduled_date for t in tasks)
        return None


# Singleton
maintenance_scheduler = MaintenanceScheduler()
```

## services/notification_service.py

**File path:** `services/notification_service.py`

```python
"""Real-time notification service."""

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class NotificationType(str, Enum):
    INCIDENT_DETECTED = "incident_detected"
    AGENTS_WORKING = "agents_working"
    AGENTS_COMPLETE = "agents_complete"
    INCIDENT_RESOLVED = "incident_resolved"
    MAINTENANCE_SCHEDULED = "maintenance_scheduled"
    REVENUE_IMPACT = "revenue_impact"


class NotificationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"


@dataclass
class Notification:
    id: str
    type: NotificationType
    severity: NotificationSeverity
    title: str
    message: str
    asset_id: Optional[str] = None
    asset_name: Optional[str] = None
    incident_type: Optional[str] = None
    revenue_impact: Optional[float] = None
    maintenance_scheduled: Optional[str] = None
    human_approval_required: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    read: bool = False
    metadata: dict = field(default_factory=dict)


class NotificationService:
    _instance = None
    _notifications: List[Notification] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def add_notification(self, notification: Notification) -> None:
        self._notifications.insert(0, notification)
        if len(self._notifications) > 100:
            self._notifications = self._notifications[:100]
        print(f"🔔 NOTIFICATION: {notification.title} - {notification.message}")
    
    def get_notifications(self, limit: int = 20, unread_only: bool = False) -> List[Notification]:
        notifications = self._notifications
        if unread_only:
            notifications = [n for n in notifications if not n.read]
        return notifications[:limit]
    
    def mark_read(self, notification_id: str) -> None:
        for n in self._notifications:
            if n.id == notification_id:
                n.read = True
                break
    
    def mark_all_read(self) -> None:
        for n in self._notifications:
            n.read = True
    
    def get_unread_count(self) -> int:
        return len([n for n in self._notifications if not n.read])


notification_service = NotificationService()
```

## services/persistence.py

**File path:** `services/persistence.py`

```python
"""Optimized persistence service with async/batch operations."""

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Any

from database.connection import get_session
from database.models import AgentExecutionDB, ExecutionReportDB, IncidentDB, TelemetryDB
from database.repositories.agent_repo import AgentRepository
from database.repositories.incident_repo import IncidentRepository
from database.repositories.report_repo import ReportRepository
from database.repositories.telemetry_repo import TelemetryRepository

logger = logging.getLogger(__name__)

# Thread pool for async persistence
_pool = ThreadPoolExecutor(max_workers=2)


class PersistenceService:
    
    def record_telemetry(self, readings):
        """Async persistence - don't block the main thread."""
        if not readings:
            return
        _pool.submit(self._record_telemetry_sync, readings)

    def _record_telemetry_sync(self, readings):
        """Sync version for background thread."""
        session = get_session()
        try:
            rows = [
                TelemetryDB(
                    asset_id=reading.asset_id,
                    sensor_type=reading.sensor_type.value,
                    value=reading.value,
                    timestamp=reading.timestamp,
                )
                for reading in readings
            ]
            TelemetryRepository(session).create_many(rows)
        except Exception:
            session.rollback()
            logger.exception("Failed to persist telemetry batch.")
        finally:
            session.close()

    def record_execution(self, event, report, severity="high"):
        """Async persistence - don't block the main thread."""
        _pool.submit(self._record_execution_sync, event, report, severity)

    def _record_execution_sync(self, event, report, severity):
        """Sync version for background thread."""
        session = get_session()
        try:
            incident = IncidentDB(
                id=event.id,
                asset_id=event.source,
                event=event.name,
                severity=severity,
                status="completed" if report.success else "requires_review",
                report=report.final_summary,
                created_at=event.timestamp,
            )
            IncidentRepository(session).create(incident)

            stored_report = ExecutionReportDB(
                id=report.id,
                execution_id=report.execution_id,
                incident_id=event.id,
                workflow=report.workflow_name,
                success=report.success,
                summary=report.final_summary,
                recommendations=report.recommendations,
                started_at=report.started_at,
                completed_at=report.completed_at,
            )
            ReportRepository(session).create(stored_report)

            agent_rows = [
                AgentExecutionDB(
                    id=result.id,
                    incident_id=event.id,
                    agent_name=result.agent_name,
                    task=result.metadata.get("task_name", ""),
                    input=result.metadata.get("task_description", ""),
                    output=result.summary,
                    success=result.success,
                    confidence=result.confidence,
                    summary=result.summary,
                    recommendations=result.recommendations,
                    decision=result.decision,
                    evidence=result.evidence,
                    actions_required=result.actions_required,
                    requires_human_approval=result.requires_human_approval,
                    timestamp=result.timestamp,
                )
                for result in report.agent_results
            ]
            if agent_rows:
                AgentRepository(session).create_many(agent_rows)
        except Exception:
            session.rollback()
            logger.exception("Failed to persist MAO execution.")
        finally:
            session.close()

    def wait_for_persistence(self):
        """Wait for all pending persistence operations to complete."""
        _pool.shutdown(wait=True)
```

## services/refinery_generator.py

**File path:** `services/refinery_generator.py`

```python
"""Generate multiple refineries with hundreds of assets."""

from typing import List, Dict
from models.asset import Asset, AssetType, Refinery
from uuid import uuid4
import random


class RefineryGenerator:
    """Generate realistic refinery assets for simulation."""

    REFINERY_NAMES = [
        "RigOS Alpha Refinery",
        "North Terminal Refinery",
        "South Coast Refinery",
        "East Valley Refinery",
        "West Port Refinery",
        "Central Hub Refinery",
        "Gulf Coast Refinery",
        "Pacific Refinery",
        "Atlantic Refinery",
        "Midwest Refinery",
    ]

    ZONES = ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E", "Zone F"]

    PUMP_NAMES = ["Pump A", "Pump B", "Pump C", "Pump D", "Pump E", "Pump F", "Pump G", "Pump H"]
    COMPRESSOR_NAMES = ["Compressor C-01", "Compressor C-02", "Compressor C-03", "Compressor C-04"]
    VALVE_NAMES = ["Valve V-01", "Valve V-02", "Valve V-03", "Valve V-04", "Valve V-05"]
    HEAT_EXCHANGER_NAMES = ["HX-01", "HX-02", "HX-03", "HX-04"]
    TANK_NAMES = ["Tank T-01", "Tank T-02", "Tank T-03", "Tank T-04"]
    REACTOR_NAMES = ["Reactor R-01", "Reactor R-02"]
    PIPELINE_NAMES = ["Pipeline P-01", "Pipeline P-02", "Pipeline P-03"]

    @classmethod
    def generate_assets_for_refinery(cls, refinery_name: str, asset_count: int = 50) -> List[Asset]:
        """Generate assets for a refinery."""
        assets = []
        refinery_id = str(uuid4())

        # Determine how many of each type
        pumps = asset_count // 5
        compressors = asset_count // 10
        valves = asset_count // 8
        heat_exchangers = asset_count // 12
        tanks = asset_count // 15
        reactors = asset_count // 20
        pipelines = asset_count // 15
        others = asset_count - (pumps + compressors + valves + heat_exchangers + tanks + reactors + pipelines)

        # Generate Pumps
        for i in range(pumps):
            name = f"Pump {chr(65 + i % 26)}-{i // 26 + 1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.PUMP,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(70, 100),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Compressors
        for i in range(compressors):
            name = f"Compressor C-{i+1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.COMPRESSOR,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(65, 98),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.6, 0.25, 0.1, 0.05])[0],
            ))

        # Generate Valves
        for i in range(valves):
            name = f"Valve V-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.VALVE,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(60, 100),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.65, 0.25, 0.08, 0.02])[0],
            ))

        # Generate Heat Exchangers
        for i in range(heat_exchangers):
            name = f"HX-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.HEAT_EXCHANGER,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(50, 95),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.5, 0.25, 0.15, 0.1])[0],
            ))

        # Generate Tanks
        for i in range(tanks):
            name = f"Tank T-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.TANK,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(70, 100),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Reactors
        for i in range(reactors):
            name = f"Reactor R-{i+1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.REACTOR,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(60, 95),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.55, 0.25, 0.15, 0.05])[0],
            ))

        # Generate Pipelines
        for i in range(pipelines):
            name = f"Pipeline P-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.PIPELINE,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(65, 100),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Other assets
        other_types = [AssetType.MOTOR, AssetType.GENERATOR, AssetType.BOILER, AssetType.TURBINE, AssetType.DISTILLATION_COLUMN]
        for i in range(others):
            asset_type = random.choice(other_types)
            name = f"{asset_type.value} {i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=asset_type,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(60, 98),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.6, 0.25, 0.1, 0.05])[0],
            ))

        return assets

    @classmethod
    def generate_refineries(cls, count: int = 5, assets_per_refinery: int = 50) -> List[Refinery]:
        """Generate multiple refineries with assets."""
        refineries = []
        selected_names = random.sample(cls.REFINERY_NAMES, min(count, len(cls.REFINERY_NAMES)))

        for name in selected_names:
            assets = cls.generate_assets_for_refinery(name, assets_per_refinery)
            refineries.append(Refinery(
                id=str(uuid4()),
                name=name,
                location=random.choice(["Texas", "Louisiana", "California", "Alaska", "Oklahoma", "Alberta"]),
                assets=assets,
                status=random.choices(["Active", "Active", "Active", "Maintenance"])[0],
            ))

        return refineries
```

## services/report.py

**File path:** `services/report.py`

```python

```

## services/revenue_impact_calculator.py

**File path:** `services/revenue_impact_calculator.py`

```python
"""Revenue impact calculation service."""

from typing import Dict, Optional
from services.ai_config import AIConfigGenerator


class RevenueService:
    """Calculate revenue impact based on asset health and incidents."""
    
    _instance = None
    
    # Revenue per asset per day (in $)
    ASSET_REVENUE = {
        "Pump": 5000,
        "Compressor": 8000,
        "Tank": 3000,
        "Valve": 2000,
        "Pipeline": 6000,
        "Heat Exchanger": 7000,
        "Reactor": 12000,
        "Boiler": 9000,
        "Turbine": 15000,
        "Motor": 4000,
        "Generator": 10000,
        "Distillation Column": 20000,
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_asset_revenue(self, asset_type: str) -> float:
        """Get daily revenue for an asset type."""
        return self.ASSET_REVENUE.get(asset_type, 5000)
    
    def calculate_asset_health_impact(self, asset_health: float, asset_type: str, 
                                       failure_probability: float, rul_days: float) -> Dict:
        """Calculate revenue impact for a single asset."""
        daily_revenue = self.get_asset_revenue(asset_type)
        
        # Health factor (0-1)
        health_factor = asset_health / 100.0
        
        # Degradation factor
        degradation_factor = max(0, min(1, (100 - asset_health) / 50))
        
        # Current revenue contribution
        current_revenue = daily_revenue * health_factor
        
        # Projected revenue loss
        projected_loss = daily_revenue * degradation_factor * 0.3
        
        # If failure is imminent (RUL < 30 days)
        if rul_days < 30:
            failure_loss = daily_revenue * (1 - health_factor) * 0.5
        else:
            failure_loss = 0
        
        total_impact = projected_loss + failure_loss
        
        return {
            "daily_revenue": daily_revenue,
            "current_contribution": round(current_revenue, 2),
            "projected_loss": round(projected_loss, 2),
            "failure_loss": round(failure_loss, 2),
            "total_impact": round(total_impact, 2),
            "health_factor": round(health_factor, 3),
            "degradation_factor": round(degradation_factor, 3),
        }
    
    def calculate_company_revenue_impact(self, assets: list) -> Dict:
        """Calculate total revenue impact across all assets."""
        total_revenue = 0
        total_current = 0
        total_projected_loss = 0
        total_failure_loss = 0
        total_health = 0
        
        for asset in assets:
            asset_type = asset.get("type", "Pump")
            health = asset.get("health", 100)
            failure_prob = asset.get("failure_probability", 0)
            rul = asset.get("rul_days", 365)
            
            result = self.calculate_asset_health_impact(
                health, asset_type, failure_prob, rul
            )
            
            total_revenue += result["daily_revenue"]
            total_current += result["current_contribution"]
            total_projected_loss += result["projected_loss"]
            total_failure_loss += result["failure_loss"]
            total_health += health
        
        avg_health = total_health / len(assets) if assets else 0
        
        return {
            "total_potential_revenue": round(total_revenue, 2),
            "current_revenue": round(total_current, 2),
            "projected_loss": round(total_projected_loss, 2),
            "failure_loss": round(total_failure_loss, 2),
            "total_impact": round(total_projected_loss + total_failure_loss, 2),
            "avg_health": round(avg_health, 1),
            "revenue_efficiency": round((total_current / total_revenue) * 100 if total_revenue else 0, 1),
        }
    
    def calculate_incident_impact(self, incident_type: str, asset_type: str, 
                                   duration_hours: float = 4) -> Dict:
        """Calculate revenue impact of a specific incident."""
        daily_revenue = self.get_asset_revenue(asset_type)
        
        # Incident severity multipliers
        severity_multipliers = {
            "Pressure Spike": 0.3,
            "High Temperature": 0.25,
            "Gas Leak": 0.5,
            "High Vibration": 0.2,
            "Flow Restriction": 0.15,
        }
        
        multiplier = severity_multipliers.get(incident_type, 0.2)
        
        # Revenue loss = daily_revenue * (duration/24) * multiplier
        revenue_loss = daily_revenue * (duration_hours / 24) * multiplier
        
        return {
            "incident_type": incident_type,
            "duration_hours": duration_hours,
            "daily_revenue": daily_revenue,
            "revenue_loss": round(revenue_loss, 2),
            "severity_multiplier": multiplier,
        }


# Singleton
revenue_service = RevenueService()
```

## services/runtime.py

**File path:** `services/runtime.py`

```python
"""Runtime module - lazy initialization with auto-start simulation."""

import time
import threading
from mao import MAOKernel
from models.asset import Asset, AssetType
from models.facility import Facility
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.flow_workflow import FlowWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow
from agents.safety import SafetyAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.diagnostic import DiagnosticAgent
from agents.planning import PlanningAgent
from agents.notification import NotificationAgent
from agents.prediction import PredictionAgent
from agents.report import ReportAgent
from agents.sensor import SensorAgent
from rag.embedder import Embedder
from rag.neon_vector_store import NeonVectorStore
from services.refinery_generator import RefineryGenerator

# Global instances
_kernel = None
_simulator = None
_refineries = None
_vector_store = None
_initialized = False
_simulation_thread = None
_simulation_running = False


def get_kernel():
    """Lazy-initialize and return the shared MAO kernel."""
    global _kernel, _initialized
    if _kernel is None:
        _kernel = _initialize_kernel()
        _initialized = True
    return _kernel


def is_initialized():
    """Check if kernel is already initialized."""
    return _initialized


def get_simulator():
    """Lazy-initialize and return the shared simulator."""
    global _simulator
    if _simulator is None:
        _simulator = _initialize_simulator()
    return _simulator


def _initialize_kernel():
    """Initialize the MAO kernel with all agents and workflows."""
    print("🚀 Initializing MAO Kernel...")
    start = time.time()
    
    # ✅ Generate AI configuration ONCE on startup
    try:
        from services.ai_config import AIConfigGenerator
        ai_config = AIConfigGenerator()
        print("✅ AI Configuration generated successfully")
    except Exception as e:
        print(f"⚠️ AI Config generation failed: {e}")
    
    kernel = MAOKernel()
    
    # Register workflows
    for workflow in (
        PressureWorkflow(),
        TemperatureWorkflow(),
        GasWorkflow(),
        FlowWorkflow(),
        MaintenanceWorkflow(),
    ):
        kernel.register_workflow(workflow)
    
    # Initialize vector store
    global _vector_store
    try:
        embedder = Embedder()
        _vector_store = NeonVectorStore(embedder.get_model())
        print("✅ Vector store initialized")
    except Exception as e:
        print(f"⚠️ Vector store failed: {e}")
        _vector_store = None
    
    # Register all agents
    for agent in (
        SafetyAgent(),
        KnowledgeAgent(_vector_store),
        MaintenanceAgent(),
        DiagnosticAgent(),
        PlanningAgent(),
        SensorAgent(),
        PredictionAgent(),
        NotificationAgent(),
        ReportAgent(),
    ):
        kernel.register_agent(agent)
    
    # Generate refineries
    global _refineries
    _refineries = RefineryGenerator.generate_refineries(count=5, assets_per_refinery=50)
    
    for refinery in _refineries:
        for asset in refinery.assets:
            kernel.asset_service.register(asset)
    
    kernel._refineries = _refineries
    
    elapsed = time.time() - start
    print(f"✅ Kernel initialized in {elapsed:.2f}s with {sum(len(r.assets) for r in _refineries)} assets")
    
    # Persist to database
    _persist_assets_to_database(kernel)
    
    # ✅ AUTO-START SIMULATION
    _start_auto_simulation(kernel)
    
    return kernel


def _start_auto_simulation(kernel):
    """Start the simulation automatically in background."""
    global _simulation_thread, _simulation_running
    
    if _simulation_running:
        return
    
    _simulation_running = True
    _simulation_thread = threading.Thread(
        target=_auto_simulation_loop,
        args=(kernel,),
        daemon=True
    )
    _simulation_thread.start()
    print("✅ Auto-simulation started in background")


def _auto_simulation_loop(kernel):
    """Background thread that runs the simulation automatically."""
    import random
    from simulator.simulator import Simulator
    from services.refinery_generator import RefineryGenerator
    
    # ✅ Create simulator
    all_assets = []
    for refinery in _refineries:
        all_assets.extend(refinery.assets)
    
    facility = Facility(
        id="rigos-alpha",
        name="RigOS Global",
        assets=all_assets
    )
    
    from simulator.facility import SimulatedFacility
    simulated_facility = SimulatedFacility(facility)
    simulator = Simulator(
        facility=simulated_facility,
        kernel=kernel
    )
    
    tick = 0
    
    while _simulation_running:
        try:
            tick += 1
            
            # ✅ Generate random fault with random intervals
            fault = None
            
            # ✅ Random incident generation (every 15-60 seconds)
            if tick % random.randint(15, 60) == 0:
                # Pick random refinery
                refinery = random.choice(_refineries)
                if refinery.assets:
                    # Pick random asset from that refinery
                    asset = random.choice(refinery.assets)
                    
                    # Pick random sensor type
                    sensor_types = ["pressure", "temperature", "vibration", "gas", "flow"]
                    sensor = random.choice(sensor_types)
                    
                    # Create fault based on sensor type
                    fault_values = {
                        "pressure": {"sensor": "pressure", "value": random.randint(155, 180)},
                        "temperature": {"sensor": "temperature", "value": random.randint(90, 110)},
                        "vibration": {"sensor": "vibration", "value": random.randint(12, 20)},
                        "gas": {"sensor": "gas", "value": random.randint(45, 70)},
                        "flow": {"sensor": "flow", "value": random.randint(10, 20)},
                    }
                    
                    fault = fault_values[sensor]
                    
                    # ✅ Only inject fault for the specific asset
                    # Find the asset index
                    for idx, sim_asset in enumerate(simulated_facility.assets):
                        if sim_asset.asset.id == asset.id:
                            # ✅ Inject fault for this specific asset
                            telemetry, reports = simulator.tick(tick, fault, target_asset_id=asset.id)
                            break
                    else:
                        # No match, run normal tick
                        telemetry, reports = simulator.tick(tick)
                else:
                    telemetry, reports = simulator.tick(tick)
            else:
                # Normal tick with random fluctuations
                telemetry, reports = simulator.tick(tick)
            
            # ✅ Update kernel state
            for reading in telemetry:
                kernel.state.add_telemetry([reading])
            
            # ✅ Update asset health
            for asset in simulated_facility.assets:
                history = kernel.state.get_history(asset.asset.id)
                if history:
                    health = kernel.health.calculate_health(history)
                    kernel.asset_service.update_health(asset.asset.id, health)
            
            # ✅ Process any incidents
            for report in reports:
                kernel.state.add_report(report)
                for result in report.agent_results:
                    kernel.state.add_agent_result(result)
            
            # ✅ Wait between ticks
            time.sleep(random.uniform(1.0, 2.5))
            
        except Exception as e:
            print(f"⚠️ Simulation error: {e}")
            time.sleep(1)


def _persist_assets_to_database(kernel):
    """Persist all assets and refineries to database."""
    try:
        from database.connection import get_session
        from database.models import AssetDB
        from database.repositories.asset_repo import AssetRepository
        
        session = get_session()
        repo = AssetRepository(session)
        
        existing = repo.get_all()
        if not existing or len(existing) == 0:
            count = 0
            for refinery in kernel._refineries:
                for asset in refinery.assets:
                    asset_db = AssetDB(
                        id=asset.id,
                        name=asset.name,
                        asset_type=asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type),
                        location=refinery.name,
                        health=asset.health,
                        status=asset.status,
                    )
                    session.add(asset_db)
                    count += 1
            session.commit()
            print(f"✅ Persisted {count} assets to database")
        else:
            print(f"✅ Assets already exist in database ({len(existing)} found)")
        
        session.close()
    except Exception as e:
        print(f"⚠️ Could not persist assets to database: {e}")


def _initialize_simulator():
    """Initialize the simulator with all assets."""
    from simulator.facility import SimulatedFacility
    from simulator.simulator import Simulator
    
    kernel = get_kernel()
    
    all_assets = []
    for refinery in _refineries:
        all_assets.extend(refinery.assets)
    
    facility = Facility(
        id="rigos-alpha",
        name="RigOS Global",
        assets=all_assets
    )
    
    simulated_facility = SimulatedFacility(facility)
    simulator = Simulator(
        facility=simulated_facility,
        kernel=kernel
    )
    
    return simulator


# Backward compatibility
class _RuntimeProxy:
    @property
    def kernel(self):
        return get_kernel()
    
    @property
    def simulator(self):
        return get_simulator()


runtime = _RuntimeProxy()
kernel = runtime.kernel
simulator = runtime.simulator
```

## services/sensor.py

**File path:** `services/sensor.py`

```python

```

## services/simulation.py

**File path:** `services/simulation.py`

```python

```

## services/simulator_controller.py

**File path:** `services/simulator_controller.py`

```python
"""Optimized Simulator controller - NO circular imports."""

import threading
import time
from typing import Dict, List, Optional, Any


class SimulatorController:
    """Controls the simulation lifecycle with UI integration and auto-refresh."""

    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.tick_count = 0
        self._latest_telemetry: List[Any] = []
        self._latest_reports: List[Any] = []
        self._config_refresh_interval = 30
        self._simulator = None
        self._kernel = None

    @property
    def simulator(self):
        """Lazy load simulator."""
        if self._simulator is None:
            from services.runtime import get_simulator
            self._simulator = get_simulator()
        return self._simulator

    @property
    def kernel(self):
        """Lazy load kernel."""
        if self._kernel is None:
            from services.runtime import get_kernel
            self._kernel = get_kernel()
        return self._kernel

    def start(self, interval: float = 1.0):
        if self.running:
            return

        self.running = True
        self.kernel._simulation_running = True
        self._thread = threading.Thread(
            target=self._run,
            args=(interval,),
            daemon=True
        )
        self._thread.start()
        print(f"✅ Simulation started with interval {interval}s")

    def stop(self):
        self.running = False
        self.kernel._simulation_running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print("⏹️ Simulation stopped")

    def step(self) -> tuple[List[Any], List[Any]]:
        self.tick_count += 1
        
        if self.tick_count % self._config_refresh_interval == 0:
            self._refresh_config()
        
        telemetry, reports = self.simulator.tick(self.tick_count)
        self._latest_telemetry = telemetry
        self._latest_reports = reports
        return telemetry, reports

    def _run(self, interval: float):
        while self.running:
            try:
                self.step()
            except Exception as e:
                print(f"⚠️ Simulation error: {e}")
                continue
            time.sleep(interval)

    def _refresh_config(self):
        try:
            from services.config_services import ConfigService
            ConfigService().clear_cache()
            
            from simulator.event_generator import EventGenerator
            EventGenerator().clear_cache()
            
            print(f"🔄 [Tick {self.tick_count}] Refreshed Gemini configuration")
        except Exception as e:
            print(f"⚠️ Config refresh failed: {e}")

    def get_latest_telemetry(self) -> List[Any]:
        return self._latest_telemetry

    def get_latest_reports(self) -> List[Any]:
        return self._latest_reports

    def get_status(self) -> Dict:
        return {
            "running": self.running,
            "ticks": self.tick_count,
            "assets": len(self.kernel.asset_service.all_assets()),
            "events": len(self.kernel.event_store.all()),
            "reports": len(self.kernel.state.execution_reports),
            "agent_results": len(self.kernel.state.agent_results),
        }


sim_controller = SimulatorController()
```

## services/telemetry_store.py

**File path:** `services/telemetry_store.py`

```python
from collections import defaultdict


class TelemetryStore:

    def __init__(self):

        self.history = defaultdict(list)

    def add(self, readings):

        for reading in readings:

            self.history[reading.asset_id].append(reading)

            if len(self.history[reading.asset_id]) > 100:

                self.history[reading.asset_id].pop(0)

    def get_asset_history(self, asset_id):

        return self.history[asset_id]
```

## services/vision.py

**File path:** `services/vision.py`

```python

```

## services/weather.py

**File path:** `services/weather.py`

```python

```
