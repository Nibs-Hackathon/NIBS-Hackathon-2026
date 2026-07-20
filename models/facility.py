from typing import List

from pydantic import BaseModel

from models.asset import Asset
from models.enums import FacilityStatus


class Facility(BaseModel):
    id: str
    name: str

    location: str

    status: FacilityStatus

    assets: List[Asset] = []