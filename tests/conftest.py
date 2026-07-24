import sys
from pathlib import Path
from unittest.mock import MagicMock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from mao.core.context import ExecutionContext
from mao.core.state_manager import StateManager
from mao.memory.memory_manager import MemoryManager
from mao.core.logger import KernelLogger


class DummyEvent:
    def __init__(self, payload):
        self.payload = payload
        self.id = "test-event-id"
        self.name = "TestEvent"
        self.source = "test-source"
        self.timestamp = None


@pytest.fixture
def normal_context():
    event = DummyEvent({
        "pressure": 120,
        "temperature": 50,
        "gas_level": 5,
        "vibration": 2,
        "flow_rate": 80,
    })
    
    return ExecutionContext(
        event,
        state_manager=StateManager(),
        memory_manager=MemoryManager(),
        logger=KernelLogger(),
        health_service=None,
    )


@pytest.fixture
def critical_context():
    event = DummyEvent({
        "pressure": 170,
        "temperature": 95,
        "gas_level": 60,
        "vibration": 10,
        "flow_rate": 20,
    })
    
    return ExecutionContext(
        event,
        state_manager=StateManager(),
        memory_manager=MemoryManager(),
        logger=KernelLogger(),
        health_service=None,
    )


@pytest.fixture
def mock_knowledge_agent():
    """Create a KnowledgeAgent with mocked retriever."""
    from agents.knowledge import KnowledgeAgent
    agent = KnowledgeAgent(MagicMock())
    agent.retriever = MagicMock()
    agent.retriever.retrieve.return_value = []
    return agent