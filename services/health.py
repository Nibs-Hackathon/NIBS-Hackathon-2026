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