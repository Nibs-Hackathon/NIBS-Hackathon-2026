"""Runtime module - lazy initialization with auto-start simulation."""

import time
import threading
import os
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
from services.local_mode import local_demo_mode


# Global instances
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


def is_initialized():
    """Check if kernel is already initialized."""
    return _initialized


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

    # Ensure operational tables exist when DATABASE_URL is configured.
    # Knowledge/pgvector is optional for local Postgres without the extension.
    try:
        from database.bootstrap import create_schema
        create_schema()
    except Exception as e:
        print(f"⚠️ Schema bootstrap skipped: {e}")
    
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
    local_store = None
    primary_store = None
    try:
        from rag.local_knowledge_store import HybridKnowledgeStore, LocalKnowledgeStore
        local_store = LocalKnowledgeStore()
        primary_store = None
        if not local_demo_mode():
            try:
                primary_store = NeonVectorStore(Embedder().get_model())
                if primary_store.count() == 0:
                    primary_store = None
            except Exception as error:
                print(f"Vector retrieval unavailable; using local refinery corpus: {type(error).__name__}")
        _vector_store = HybridKnowledgeStore(primary=primary_store, fallback=local_store)
        print("✅ Vector store initialized")
    except Exception as e:
        print(f"⚠️ Vector store failed: {e}")
        from rag.local_knowledge_store import LocalKnowledgeStore
        _vector_store = LocalKnowledgeStore()
    
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

    kernel._knowledge_document_count = local_store.count() if local_store is not None else 0
    kernel._knowledge_source = "local_corpus+vector" if primary_store is not None else "local_corpus"
    
    # Generate refineries
    global _refineries
    # Populate every catalog facility. Twenty-four assets per site keeps the
    # full 16-site portfolio bounded at 384 simulated assets.
    _refineries = RefineryGenerator.generate_refineries(
        count=len(RefineryGenerator.REFINERY_NAMES),
        assets_per_refinery=24,
    )
    
    for refinery in _refineries:
        for asset in refinery.assets:
            kernel.asset_service.register(asset)
    
    kernel._refineries = _refineries
    
    elapsed = time.time() - start
    print(f"✅ Kernel initialized in {elapsed:.2f}s with {sum(len(r.assets) for r in _refineries)} assets")
    
    # Persist to database
    _persist_assets_to_database(kernel)
    
    # ✅ AUTO-START SIMULATION (but don't block)
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
    """Run bounded telemetry plus fair, automatic portfolio incident scenarios."""
    import math
    import random
    from datetime import datetime, timedelta

    global _simulator

    from simulator.facility import SimulatedFacility
    from simulator.simulator import Simulator

    all_assets = [asset for refinery in _refineries for asset in refinery.assets]
    facility = Facility(id="rigos-global", name="RigOS Global", assets=all_assets)
    simulated_facility = SimulatedFacility(facility)
    simulator = Simulator(facility=simulated_facility, kernel=kernel)
    _simulator = simulator

    tick_interval = max(0.5, float(os.getenv("RIGOS_SIMULATION_TICK_SECONDS", "2")))
    warmup_seconds = max(2.0, float(os.getenv("RIGOS_SIMULATION_WARMUP_SECONDS", "8")))
    initial_delay = max(1, int(os.getenv("RIGOS_INITIAL_INCIDENT_DELAY", "5")))
    coverage_delay = max(5, int(os.getenv("RIGOS_COVERAGE_INCIDENT_DELAY", "12")))
    regular_min_delay = max(15, int(os.getenv("RIGOS_INCIDENT_MIN_DELAY", "45")))
    regular_max_delay = max(
        regular_min_delay,
        int(os.getenv("RIGOS_INCIDENT_MAX_DELAY", "90")),
    )
    max_active = max(1, int(os.getenv("RIGOS_MAX_ACTIVE_INCIDENTS", "3")))
    auto_incidents = os.getenv("RIGOS_AUTO_INCIDENTS", "true").strip().lower() not in {
        "0", "false", "no", "off",
    }
    rng = random.Random("rigos-portfolio-scenarios")
    sensor_sequence = ["pressure", "temperature", "vibration", "gas", "flow"]
    tick = 0
    incident_counter = 0
    refinery_cursor = 0
    covered_facilities = set()

    kernel._simulation_stats = {
        "automatic": auto_incidents,
        "mode": "portfolio_rotation",
        "state": "warming_up",
        "tick_seconds": tick_interval,
        "incidents_generated": 0,
        "facilities_covered": 0,
        "coverage_complete": False,
        "portfolio_facilities": len(_refineries),
        "next_facility": _refineries[0].name if _refineries else None,
        "next_incident_at": None,
    }

    warmup_ticks = max(1, math.ceil(warmup_seconds / tick_interval))
    try:
        for _ in range(warmup_ticks):
            if not _simulation_running:
                return
            tick += 1
            simulator.tick(tick)
            time.sleep(tick_interval)
    except Exception as error:
        print(f"Simulation warm-up error: {error}")

    kernel._simulation_stats["state"] = "running" if auto_incidents else "telemetry_only"
    print(
        f"Simulation ready: telemetry every {tick_interval:g}s; "
        f"automatic portfolio incidents {'enabled' if auto_incidents else 'disabled'}."
    )

    while _simulation_running:
        try:
            first_coverage_pass = len(covered_facilities) < len(_refineries)
            if incident_counter == 0:
                wait_seconds = initial_delay
            elif first_coverage_pass:
                wait_seconds = coverage_delay
            else:
                wait_seconds = rng.randint(regular_min_delay, regular_max_delay)

            next_refinery = _refineries[refinery_cursor % len(_refineries)] if _refineries else None
            kernel._simulation_stats.update({
                "next_facility": getattr(next_refinery, "name", None),
                "next_incident_at": (
                    datetime.now() + timedelta(seconds=wait_seconds)
                ).isoformat() if auto_incidents else None,
            })

            wait_ticks = max(1, math.ceil(wait_seconds / tick_interval))
            for _ in range(wait_ticks):
                if not _simulation_running:
                    return
                tick += 1
                simulator.tick(tick)
                time.sleep(tick_interval)

            if not auto_incidents or not next_refinery:
                continue
            if len(simulator.active_incidents) >= max_active:
                continue

            available_assets = [
                asset for asset in next_refinery.assets
                if asset.id not in simulator.active_incidents
            ]
            if not available_assets:
                continue

            asset = rng.choice(available_assets)
            sensor = sensor_sequence[incident_counter % len(sensor_sequence)]
            fault_values = {
                "pressure": {"sensor": "pressure", "value": rng.randint(155, 180)},
                "temperature": {"sensor": "temperature", "value": rng.randint(90, 110)},
                "vibration": {"sensor": "vibration", "value": rng.randint(12, 20)},
                "gas": {"sensor": "gas", "value": rng.randint(45, 70)},
                "flow": {"sensor": "flow", "value": rng.randint(10, 20)},
            }
            simulator.tick(tick, fault_values[sensor], target_asset_id=asset.id)
            incident_counter += 1
            refinery_cursor += 1
            covered_facilities.add(next_refinery.id)
            kernel._simulation_stats.update({
                "incidents_generated": incident_counter,
                "facilities_covered": len(covered_facilities),
                "coverage_complete": len(covered_facilities) == len(_refineries),
                "last_facility": next_refinery.name,
                "last_asset_id": asset.id,
                "last_asset_name": asset.name,
                "last_incident_type": sensor,
                "last_incident_at": datetime.now().isoformat(),
            })
            print(
                f"Automatic scenario #{incident_counter}: {sensor} fault on "
                f"{next_refinery.name} / {asset.name}"
            )
        except Exception as error:
            print(f"Simulation loop recovered from {type(error).__name__}: {error}")
            time.sleep(tick_interval)


def _persist_assets_to_database(kernel):
    """Persist all assets and refineries to database."""
    if local_demo_mode():
        print("Local demo mode: database persistence disabled")
        return

    try:
        from database.connection import get_session
        from database.models import AssetDB
        from database.repositories.asset_repo import AssetRepository
        
        session = get_session()
        repo = AssetRepository(session)
        
        existing = repo.get_all()
        existing_ids = {str(asset.id) for asset in existing}
        if existing is not None:
            count = 0
            for refinery in kernel._refineries:
                for asset in refinery.assets:
                    if str(asset.id) in existing_ids:
                        continue
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


# ✅ Runtime proxy for lazy loading
class _RuntimeProxy:
    @property
    def kernel(self):
        return get_kernel()
    
    @property
    def simulator(self):
        return get_simulator()

    @property
    def active_simulator(self):
        """Return the timer-driven simulator without creating a second one."""
        return _simulator


# ✅ Export runtime - the single entry point
runtime = _RuntimeProxy()
