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
        """Calculate a transparent, deterministic incident economics estimate."""
        daily_revenue = self.get_asset_revenue(asset_type)
        
        # Incident severity multipliers
        severity_multipliers = {
            "pressurespike": 0.3,
            "hightemperature": 0.25,
            "gasleak": 0.5,
            "highvibration": 0.2,
            "flowrestriction": 0.15,
        }
        normalized_incident = "".join(
            character for character in str(incident_type or "").lower()
            if character.isalnum()
        )
        multiplier = severity_multipliers.get(normalized_incident, 0.2)
        
        # Revenue loss = daily_revenue * (duration/24) * multiplier
        revenue_loss = daily_revenue * (duration_hours / 24) * multiplier
        # Planning estimates, not booked finance values. Keeping these in the
        # same service ensures reports, forecasting, and Copilot use one model.
        maintenance_cost = max(
            750,
            daily_revenue * (0.08 + multiplier * 0.22) + duration_hours * 175,
        )
        production_impact_pct = min(100, multiplier * 20)
        
        return {
            "incident_type": incident_type,
            "duration_hours": duration_hours,
            "daily_revenue": daily_revenue,
            "revenue_loss": round(revenue_loss, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "production_impact_pct": round(production_impact_pct, 1),
            "severity_multiplier": multiplier,
            "provenance": "modeled_estimate",
        }


# Singleton
revenue_service = RevenueService()
