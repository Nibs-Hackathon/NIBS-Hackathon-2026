from uuid import uuid4

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    description: str

    assigned_agent: str

    completed: bool = False