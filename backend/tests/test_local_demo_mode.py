from services.ai_config import AIConfigGenerator
from services.config_services import ConfigService


EXPECTED_SEQUENCE = [
    "sensor",
    "safety",
    "diagnostic",
    "maintenance",
    "planning",
    "knowledge",
    "prediction",
    "notification",
    "report",
]


def test_local_demo_mode_uses_deterministic_configuration(monkeypatch):
    monkeypatch.setenv("LOCAL_DEMO_MODE", "true")

    AIConfigGenerator._instance = None
    AIConfigGenerator._config = None
    ConfigService._instance = None
    ConfigService._cache = {}
    ConfigService._precomputed = {}
    ConfigService._precomputed_done = False

    ai_config = AIConfigGenerator()
    config = ConfigService()

    assert ai_config.llm is None
    assert config.llm is None
    assert ai_config.get_workflow_sequence("pressure_spike") == EXPECTED_SEQUENCE
    assert config.get_workflow_sequence("pressure_spike") == EXPECTED_SEQUENCE
    assert config.get_thresholds("Pump")["pressure_max"] == 150

    AIConfigGenerator._instance = None
    AIConfigGenerator._config = None
    ConfigService._instance = None
    ConfigService._cache = {}
    ConfigService._precomputed = {}
    ConfigService._precomputed_done = False
