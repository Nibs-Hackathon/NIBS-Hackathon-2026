from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from mao.models.result import AgentResult


class ExecutionReport(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    execution_id: str

    workflow_name: str

    success: bool

    started_at: datetime

    completed_at: datetime

    agent_results: list[AgentResult]

    final_summary: str

    recommendations: list[str] = Field(default_factory=list)