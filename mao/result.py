from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    agent_name: str

    success: bool = True

    confidence: float

    summary: str

    recommendations: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    execution_time: float = 0.0

    timestamp: datetime = Field(default_factory=datetime.now)