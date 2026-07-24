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
        self._kernel = None  # ✅ Will be set lazily
    
    @property
    def kernel(self):
        """Lazy load kernel to avoid circular imports."""
        if self._kernel is None:
            from services.runtime import runtime
            self._kernel = runtime.kernel
        return self._kernel
    
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
                values.append(reading.value * 0.5)
        
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
        degradation_rate = max(0.1, min(2.0, rate + base_rate * 0.5))
        
        return degradation_rate
    
    def _calculate_failure_probability(self, health: float, degradation_rate: float) -> float:
        """Calculate failure probability from health and degradation."""
        health_factor = (100 - health) / 100
        degradation_factor = min(1, degradation_rate / 1.0)
        probability = health_factor * 0.7 + degradation_factor * 0.3
        probability = 1 - math.exp(-probability * 3)
        return min(100, max(0, probability * 100))
    
    def _calculate_rul(self, health: float, degradation_rate: float) -> float:
        """Calculate Remaining Useful Life in days."""
        if degradation_rate <= 0:
            return 365
        rul = health / (degradation_rate * 5)
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