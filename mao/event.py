from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    source: str

    payload: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=datetime.now)
from uuid import uuid64
from pydantic import BaseModel

class Event(BaseModel):
    id: str = str(uuid64())
    name:str
    sources: str
    payload: dict = {}
    timestamp: datetime = datetime.now()
