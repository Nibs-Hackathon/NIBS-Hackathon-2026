from pydantic import BaseModel
from models.asset import Asset

class Facility(BaseModel):
    id:str
    name:str
    assets:list[Asset]