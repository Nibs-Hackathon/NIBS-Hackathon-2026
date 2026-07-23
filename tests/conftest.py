import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from mao.core.context import ExecutionContext


class DummyEvent:
    def __init__(self, payload):
        self.payload = payload


@pytest.fixture
def normal_context():
    event = DummyEvent(
        {
            "pressure": 120,
            "temperature": 50,
            "gas_level": 5,
            "vibration": 2,
            "flow_rate": 80,
        }
    )

    return ExecutionContext(
        event,
        state_manager=None,
        memory_manager=None,
        logger=None,
    )


@pytest.fixture
def critical_context():

    event = DummyEvent(
        {
            "pressure": 170,
            "temperature": 95,
            "gas_level": 60,
            "vibration": 10,
            "flow_rate": 20,
        }
    )

    return ExecutionContext(
        event,
        state_manager=None,
        memory_manager=None,
        logger=None,
    )