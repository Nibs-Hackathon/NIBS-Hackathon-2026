from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional, List


class AssetType(str, Enum):
    PUMP = "Pump"
    COMPRESSOR = "Compressor"
    PIPELINE = "Pipeline"
    VALVE = "Valve"
    TANK = "Tank"
    HEAT_EXCHANGER = "Heat Exchanger"
    REACTOR = "Reactor"
    DISTILLATION_COLUMN = "Distillation Column"
    BOILER = "Boiler"
    TURBINE = "Turbine"
    MOTOR = "Motor"
    GENERATOR = "Generator"
    HVAC = "HVAC"


class AssetStatus(str, Enum):
    RUNNING = "Running"
    HEALTHY = "Healthy"
    WARNING = "Warning"
    CRITICAL = "Critical"
    OFFLINE = "Offline"
    MAINTENANCE = "Maintenance"


class Asset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    asset_type: AssetType
    refinery_id: str  # ✅ Link to refinery
    location: str
    zone: str = "Unassigned"
    health: float = 100.0
    status: str = "Running"
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class Refinery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    location: str
    assets: List[Asset] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "Active"
    metadata: dict = Field(default_factory=dict)