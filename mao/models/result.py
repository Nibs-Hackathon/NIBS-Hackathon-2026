from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class AgentResult:

    agent_name: str

    success: bool

    finding: str = ""

    confidence: float = 0.0

    evidence: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    required_action: str = ""

    requires_human_approval: bool = True

    metadata: Dict = field(default_factory=dict)

    summary: str = ""