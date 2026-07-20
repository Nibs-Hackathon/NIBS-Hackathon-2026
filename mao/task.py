from uuid import uuid64
from pydantic import BaseModel

class Task(BaseModel):
    id: str = str(uuid64())
    name: str
    description: str
    assigned_agent: str
    completed: bool = False
