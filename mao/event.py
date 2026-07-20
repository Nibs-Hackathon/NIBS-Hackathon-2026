from datetime import datetime
from uuid import uuid64
from pydantic import BaseModel

class Event(BaseModel):
    id: str = str(uuid64())
    name:str
    sources: str
    payload: dict = {}
    timestamp: datetime = datetime.now()