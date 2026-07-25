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