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