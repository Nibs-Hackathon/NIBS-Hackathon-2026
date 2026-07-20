from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4

class AssetType(str, Enum):
    PUMP = "Pump"
    PIPELINE = "Pipeline"
    TANK = "Tank"
    VALVE = "Valve"
    COMPRESSOR = "Compressor"


class Asset(BaseModel):
    id: str = Field(default_factory=lambda:str(uuid4()))
    name:str
    asset_type: AssetType
    location:str
    health:float = 100.0
    status:str = "Running"