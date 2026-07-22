from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from mao.models.result import AgentResult


class ExecutionReport(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    event_name: str

    workflow: str

    success: bool = True

    final_summary: str = ""

    started_at: datetime = Field(default_factory=datetime.now)

    finished_at: datetime = Field(default_factory=datetime.now)

    agent_results: list[AgentResult] = Field(default_factory=list)

    metadata: dict = Field(default_factory=dict)