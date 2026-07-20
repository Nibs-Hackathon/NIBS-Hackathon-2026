from typing import Optional

from pydantic import BaseModel

from models.enums import AssetStatus, AssetType
from models.sensor import SensorReading


class Asset(BaseModel):
    id: str
    name: str

    asset_type: AssetType

    location: str

    health_score: float

    status: AssetStatus

    latest_sensor: Optional[SensorReading] = None