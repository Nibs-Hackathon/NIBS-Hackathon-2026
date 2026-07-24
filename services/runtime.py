"""Runtime module - lazy initialization with auto-start simulation."""

import time
import threading
from mao import MAOKernel
from models.asset import Asset, AssetType
from models.facility import Facility
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

# Global instances - these are the REAL instances
_kernel = None
_simulator = None
_refineries = None
_vector_store = None
_initialized = False
_simulation_thread = None
_simulation_running = False


def get_kernel():
    """Lazy-initialize and return the shared MAO kernel."""
    global _kernel, _initialized
    if _kernel is None:
        _kernel = _initialize_kernel()
        _initialized = True
    return _kernel


def get_simulator():
    """Lazy-initialize and return the shared simulator."""
    global _simulator
    if _simulator is None:
        _simulator = _initialize_simulator()
    return _simulator


def _initialize_kernel():
    """Initialize the MAO kernel with all agents and workflows."""
    print("🚀 Initializing MAO Kernel...")
    start = time.time()
    
    # ✅ Generate AI configuration ONCE on startup
    try:
        from services.ai_config import AIConfigGenerator
        ai_config = AIConfigGenerator()
        print("✅ AI Configuration generated successfully")
    except Exception as e:
        print(f"⚠️ AI Config generation failed: {e}")
    
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
    
    # Initialize vector store
    global _vector_store
    try:
        embedder = Embedder()
        _vector_store = NeonVectorStore(embedder.get_model())
        print("✅ Vector store initialized")
    except Exception as e:
        print(f"⚠️ Vector store failed: {e}")
        _vector_store = None
    
    # Register all agents
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
    
    # Generate refineries
    global _refineries
    _refineries = RefineryGenerator.generate_refineries(count=5, assets_per_refinery=50)
    
    for refinery in _refineries:
        for asset in refinery.assets:
            kernel.asset_service.register(asset)
    
    kernel._refineries = _refineries
    
    elapsed = time.time() - start
    print(f"✅ Kernel initialized in {elapsed:.2f}s with {sum(len(r.assets) for r in _refineries)} assets")
    
    # Persist to database
    _persist_assets_to_database(kernel)
    
    # ✅ AUTO-START SIMULATION
    _start_auto_simulation(kernel)
    
    return kernel


def _start_auto_simulation(kernel):
    """Start the simulation automatically in background."""
    global _simulation_thread, _simulation_running
    
    if _simulation_running:
        return
    
    _simulation_running = True
    _simulation_thread = threading.Thread(
        target=_auto_simulation_loop,
        args=(kernel,),
        daemon=True
    )
    _simulation_thread.start()
    print("✅ Auto-simulation started in background")


def _auto_simulation_loop(kernel):
    """Background thread that runs the simulation automatically."""
    import random
    
    from simulator.simulator import Simulator
    from simulator.facility import SimulatedFacility
    
    # ✅ Create simulator
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
    
    tick = 0
    
    # ✅ WARM-UP - 30 ticks with no faults
    print("🔄 Simulation warming up...")
    for _ in range(30):
        tick += 1
        telemetry, reports = simulator.tick(tick)
        for reading in telemetry:
            kernel.state.add_telemetry([reading])
        for asset in simulated_facility.assets:
            history = kernel.state.get_history(asset.asset.id)
            if history:
                health = kernel.health.calculate_health(history)
                kernel.asset_service.update_health(asset.asset.id, health)
        time.sleep(0.05)
    
    print("✅ Simulation running. Faults every 45-120 seconds.")
    
    # ✅ Run with very infrequent faults
    while _simulation_running:
        try:
            tick += 1
            
            # ✅ Fault every 45-120 ticks (much less frequent)
            should_fault = tick % random.randint(45, 120) == 0 and tick > 30
            
            fault = None
            if should_fault:
                refinery = random.choice(_refineries)
                if refinery.assets:
                    asset = random.choice(refinery.assets)
                    sensor_types = ["pressure", "temperature", "vibration", "gas", "flow"]
                    sensor = random.choice(sensor_types)
                    
                    fault_values = {
                        "pressure": {"sensor": "pressure", "value": random.randint(155, 180)},
                        "temperature": {"sensor": "temperature", "value": random.randint(90, 110)},
                        "vibration": {"sensor": "vibration", "value": random.randint(12, 20)},
                        "gas": {"sensor": "gas", "value": random.randint(45, 70)},
                        "flow": {"sensor": "flow", "value": random.randint(10, 20)},
                    }
                    
                    fault = fault_values[sensor]
                    
                    # ✅ Inject fault for specific asset
                    for sim_asset in simulated_facility.assets:
                        if sim_asset.asset.id == asset.id:
                            telemetry, reports = simulator.tick(tick, fault, target_asset_id=asset.id)
                            break
                    else:
                        telemetry, reports = simulator.tick(tick)
                else:
                    telemetry, reports = simulator.tick(tick)
            else:
                telemetry, reports = simulator.tick(tick)
            
            # ✅ Update state
            for reading in telemetry:
                kernel.state.add_telemetry([reading])
            
            for asset in simulated_facility.assets:
                history = kernel.state.get_history(asset.asset.id)
                if history:
                    health = kernel.health.calculate_health(history)
                    kernel.asset_service.update_health(asset.asset.id, health)
            
            for report in reports:
                kernel.state.add_report(report)
                for result in report.agent_results:
                    kernel.state.add_agent_result(result)
            
            # ✅ Wait between ticks (slower = more stable)
            time.sleep(random.uniform(0.8, 1.5))
            
        except Exception as e:
            print(f"⚠️ Simulation error: {e}")
            time.sleep(2)
def _persist_assets_to_database(kernel):
    """Persist all assets and refineries to database."""
    try:
        from database.connection import get_session
        from database.models import AssetDB
        from database.repositories.asset_repo import AssetRepository
        
        session = get_session()
        repo = AssetRepository(session)
        
        existing = repo.get_all()
        if not existing or len(existing) == 0:
            count = 0
            for refinery in kernel._refineries:
                for asset in refinery.assets:
                    asset_db = AssetDB(
                        id=asset.id,
                        name=asset.name,
                        asset_type=asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type),
                        location=refinery.name,
                        health=asset.health,
                        status=asset.status,
                    )
                    session.add(asset_db)
                    count += 1
            session.commit()
            print(f"✅ Persisted {count} assets to database")
        else:
            print(f"✅ Assets already exist in database ({len(existing)} found)")
        
        session.close()
    except Exception as e:
        print(f"⚠️ Could not persist assets to database: {e}")


def _initialize_simulator():
    """Initialize the simulator with all assets."""
    # ✅ LAZY IMPORT inside function - breaks circular import
    from simulator.facility import SimulatedFacility
    from simulator.simulator import Simulator
    
    kernel = get_kernel()
    
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


# ✅ Runtime proxy - this is the ONLY thing we export
class _RuntimeProxy:
    @property
    def kernel(self):
        return get_kernel()
    
    @property
    def simulator(self):
        return get_simulator()


# ✅ This is the single entry point - use this everywhere
runtime = _RuntimeProxy()

# ❌ DO NOT add these lines - they cause circular imports:
# kernel = runtime.kernel
# simulator = runtime.simulator