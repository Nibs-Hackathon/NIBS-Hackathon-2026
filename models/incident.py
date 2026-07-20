from datetime import datetime

from pydantic import BaseModel

from models.enums import IncidentSeverity


class Incident(BaseModel):
    id: str

    asset_id: str

    title: str

    description: str

    severity: IncidentSeverity

    detected_at: datetime

    resolved: bool = False