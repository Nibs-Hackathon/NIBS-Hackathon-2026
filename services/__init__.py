"""Services module exports - NO circular imports."""

# ✅ Lazy imports to avoid circular issues
def get_asset_service():
    from services.asset import AssetService
    return AssetService

def get_health_service():
    from services.health import HealthService
    return HealthService

def get_llm_manager():
    from services.llm import LLMManager
    return LLMManager

def get_persistence_service():
    from services.persistence import PersistenceService
    return PersistenceService

def get_config_service():
    from services.config_services import ConfigService
    return ConfigService

def get_simulator_controller():
    from services.simulator_controller import SimulatorController, sim_controller
    return SimulatorController, sim_controller

def get_runtime():
    from services.runtime import kernel, simulator
    return kernel, simulator

def get_ai_config():
    """Get the AI Configuration Generator (singleton)."""
    from services.ai_config import AIConfigGenerator
    return AIConfigGenerator()

def get_computation_engine():
    """Get the Computation Engine (singleton)."""
    from services.computation_engine import ComputationEngine
    return ComputationEngine()


# ✅ Direct imports (safe ones - no circular issues)
from services.asset import AssetService
from services.health import HealthService
from services.llm import LLMManager
from services.persistence import PersistenceService
from services.config_services import ConfigService
from services.simulator_controller import SimulatorController, sim_controller
from services.ai_config import AIConfigGenerator
from services.computation_engine import ComputationEngine

# ✅ LAZY LOAD - Don't import kernel/simulator at module level!
# Remove this line that causes circular import:
# from services.runtime import kernel, simulator

__all__ = [
    "AssetService",
    "HealthService",
    "LLMManager",
    "PersistenceService",
    "ConfigService",
    "SimulatorController",
    "sim_controller",
    "AIConfigGenerator",
    "ComputationEngine",
    "get_ai_config",
    "get_computation_engine",
    # "kernel",  # REMOVED - causes circular import
    # "simulator",  # REMOVED - causes circular import
]