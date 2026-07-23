# Folder: scripts Code Inventory

Generated: 2026-07-23 12:30:25 UTC

Contains 10 project files.

## scripts/benchmark.py

**File path:** `scripts/benchmark.py`

```python

```

## scripts/build_rag.py

**File path:** `scripts/build_rag.py`

```python
from pathlib import Path

from rag.pipeline import RAGPipeline

docs_folder = Path("docs")

pdfs = [str(pdf) for pdf in docs_folder.glob("*.pdf")]

pipeline = RAGPipeline()

pipeline.build(pdfs)

print("✅ FAISS index created successfully!")
```

## scripts/generate_embeddings.py

**File path:** `scripts/generate_embeddings.py`

```python

```

## scripts/ingest_documents.py

**File path:** `scripts/ingest_documents.py`

```python

```

## scripts/run_simulation.py

**File path:** `scripts/run_simulation.py`

```python
import time
from uuid import uuid4

from mao import MAOKernel

from models.asset import Asset, AssetType
from models.facility import Facility

from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator


from tests.mock_workflow import MockWorkflow

from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow
from mao.workflows.flow_workflow import FlowWorkflow

from agents.safety import SafetyAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.diagnostic import DiagnosticAgent
from agents.planning import PlanningAgent



# -----------------------------
# Create Assets
# -----------------------------

pump_a = Asset(
    name="Pump A",
    asset_type=AssetType.PUMP,
    location="Zone A",
)

pump_b = Asset(
    name="Pump B",
    asset_type=AssetType.PUMP,
    location="Zone A",
)

tank_a = Asset(
    name="Tank A",
    asset_type=AssetType.TANK,
    location="Zone B",
)


facility = Facility(
    id=str(uuid4()),
    name="RigOS Alpha",
    assets=[
        pump_a,
        pump_b,
        tank_a,
    ],
)



# -----------------------------
# Setup MAO
# -----------------------------

kernel = MAOKernel()


# Register assets

for asset in facility.assets:

    kernel.asset_service.register(asset)



# Register workflows

kernel.register_workflow(MockWorkflow())

kernel.register_workflow(PressureWorkflow())
kernel.register_workflow(TemperatureWorkflow())
kernel.register_workflow(GasWorkflow())
kernel.register_workflow(MaintenanceWorkflow())
kernel.register_workflow(FlowWorkflow())



# Register agents

kernel.register_agent(SafetyAgent())
kernel.register_agent(KnowledgeAgent())
kernel.register_agent(MaintenanceAgent())
kernel.register_agent(DiagnosticAgent())
kernel.register_agent(PlanningAgent())



# -----------------------------
# Simulator
# -----------------------------

facility_sim = SimulatedFacility(facility)


simulator = Simulator(
    facility=facility_sim,
    kernel=kernel,
)



print("=" * 60)
print("🏭 RigOS Alpha Refinery")
print("=" * 60)


tick = 0


while True:

    tick += 1


    telemetry, reports = simulator.tick(tick)


    print(f"\nTick {tick}")
    print("-" * 50)



    for reading in telemetry:

        print(
            f"{reading.sensor_type.value:<12}"
            f"{reading.value:>8.2f}"
        )



    if reports:

        print("\n🚨 INCIDENT DETECTED")


        for report in reports:

            print(report.final_summary)



    print("\nRegistered Agents")


    for agent in kernel.registry.all():

        print("-", agent.name)



    print("\nTelemetry History")


    for asset in facility.assets:


        history = kernel.state.get_history(asset.id)


        print(
            f"{asset.name:<10} -> {len(history)} readings"
        )



    print("\nAsset Health")


    for asset in facility.assets:


        history = kernel.state.get_history(asset.id)


        health = kernel.health.calculate_health(history)


        kernel.asset_service.update_health(
            asset.id,
            health
        )


        asset_obj = kernel.asset_service.get(asset.id)


        print(
            f"{asset_obj.name:<10}"
            f"{asset_obj.health:>7.1f}%   "
            f"{asset_obj.status}"
        )



    print("\nMemory")


    print(
        "Events:",
        len(kernel.memory.events)
    )


    print(
        "Reports:",
        len(kernel.memory.execution_reports)
    )


    print(
        "Agent Results:",
        len(kernel.memory.agent_results)
    )



    time.sleep(1)
```

## scripts/seed_database.py

**File path:** `scripts/seed_database.py`

```python

```

## scripts/test_knowledge.py

**File path:** `scripts/test_knowledge.py`

```python
from agents.knowledge import KnowledgeAgent


agent = KnowledgeAgent()


class Task:

    description = (
        "What should operators do during a pressure spike?"
    )


result = agent.execute(Task())


print("="*60)
print(result.summary)
print("="*60)
```

## scripts/test_mao.py

**File path:** `scripts/test_mao.py`

```python
from agents.safety import SafetyAgent
from mao.events.event import Event
from mao.orchestrator import MAO

mao = MAO()

safety = SafetyAgent()

mao.register_agent(safety)

mao.event_bus.subscribe(
    "PressureSpike",
    safety.execute,
)

event = Event(
    name="PressureSpike",
    source="SensorAgent",
    payload={
        "asset": "Pump A",
        "pressure": 112,
    },
)

mao.publish(event)

mao.run()
```

## scripts/test_models.py

**File path:** `scripts/test_models.py`

```python
from datetime import datetime

from models.asset import Asset
from models.enums import AssetStatus, AssetType
from models.sensor import SensorReading

sensor = SensorReading(
    pressure=103.5,
    temperature=87.2,
    flow_rate=1200,
    vibration=0.42,
    gas_level=1.5,
    timestamp=datetime.now(),
)

pump = Asset(
    id="PUMP-001",
    name="Main Feed Pump",
    asset_type=AssetType.PUMP,
    location="Zone A",
    health_score=98.2,
    status=AssetStatus.HEALTHY,
    latest_sensor=sensor,
)

print(pump.model_dump_json(indent=2))
```

## scripts/test_rag.py

**File path:** `scripts/test_rag.py`

```python
from rag.embedder import Embedder
from rag.vector_store import VectorStore
from rag.retriever import Retriever

embedder = Embedder()

store = VectorStore(embedder)
store.load()

retriever = Retriever(store.db)

results = retriever.retrieve(
    "How do I respond to a pressure spike?"
)

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content)
```
