"""Runtime module - lazy initialization to avoid import side effects."""

from mao import MAOKernel
from models.asset import Asset, AssetType
from models.facility import Facility
from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.flow_workflow import FlowWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow
from agents.safety import SafetyAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.diagnostic import DiagnosticAgent
from agents.planning import PlanningAgent
from agents.notification import NotificationAgent
from agents.prediction import PredictionAgent
from agents.report import ReportAgent
from agents.sensor import SensorAgent
from rag.embedder import Embedder
from rag.neon_vector_store import NeonVectorStore
from services.refinery_generator import RefineryGenerator

# Global instances (lazy initialization)
_kernel = None
_simulator = None
_refineries = None
_vector_store = None


def get_kernel():
    """Lazy-initialize and return the shared MAO kernel."""
    global _kernel
    if _kernel is None:
        _kernel = _initialize_kernel()
    return _kernel


def get_simulator():
    """Lazy-initialize and return the shared simulator."""
    global _simulator
    if _simulator is None:
        _simulator = _initialize_simulator()
    return _simulator


def _initialize_kernel():
    """Initialize the MAO kernel with all agents and workflows."""
    kernel = MAOKernel()
    
    # Register workflows
    for workflow in (
        PressureWorkflow(),
        TemperatureWorkflow(),
        GasWorkflow(),
        FlowWorkflow(),
        MaintenanceWorkflow(),
    ):
        kernel.register_workflow(workflow)
    
    # Initialize vector store for Knowledge Agent
    global _vector_store
    embedder = Embedder()
    _vector_store = NeonVectorStore(embedder.get_model())
    
    # Register all 9 agents
    for agent in (
        SafetyAgent(),
        KnowledgeAgent(_vector_store),
        MaintenanceAgent(),
        DiagnosticAgent(),
        PlanningAgent(),
        SensorAgent(),
        PredictionAgent(),
        NotificationAgent(),
        ReportAgent(),
    ):
        kernel.register_agent(agent)
    
    # Generate and register refineries
    global _refineries
    _refineries = RefineryGenerator.generate_refineries(count=5, assets_per_refinery=50)
    
    for refinery in _refineries:
        for asset in refinery.assets:
            kernel.asset_service.register(asset)
    
    kernel._refineries = _refineries
    
    print(f"✅ Initialized {len(_refineries)} refineries with {sum(len(r.assets) for r in _refineries)} assets")
    
    return kernel


def _initialize_simulator():
    """Initialize the simulator with all assets."""
    kernel = get_kernel()
    
    # Create facility with all assets
    all_assets = []
    for refinery in _refineries:
        all_assets.extend(refinery.assets)
    
    facility = Facility(
        id="rigos-alpha",
        name="RigOS Global",
        assets=all_assets
    )
    
    simulated_facility = SimulatedFacility(facility)
    simulator = Simulator(
        facility=simulated_facility,
        kernel=kernel
    )
    
    return simulator


# Backward compatibility - lazy properties
class _RuntimeProxy:
    """Proxy that lazily loads kernel and simulator."""
    
    @property
    def kernel(self):
        return get_kernel()
    
    @property
    def simulator(self):
        return get_simulator()


# Replace direct imports with proxy
runtime = _RuntimeProxy()
kernel = runtime.kernel
simulator = runtime.simulator