"""Runtime-only notification model for MAO workflow outputs."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Notification:
    """A structured operator notification held in StateManager memory."""

    source: str
    severity: str
    summary: str
    asset_id: str | None = None
    requires_human_approval: bool = False
    metadata: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
