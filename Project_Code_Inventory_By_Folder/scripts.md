# Folder: scripts Code Inventory

Generated: 2026-07-24 12:23:53 UTC

Contains 12 project files.

## scripts/benchmark.py

**File path:** `scripts/benchmark.py`

```python

```

## scripts/build_knowledge.py

**File path:** `scripts/build_knowledge.py`

```python
"""Build the Neon/pgvector knowledge index used by the Streamlit UI."""

import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(
        str(ROOT_DIR)
    )


from rag.ingestion import KnowledgeIngestion


def parse_args():
    parser = argparse.ArgumentParser(
        description="Index PDF knowledge documents into the configured Neon database."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=ROOT_DIR / "docs",
        help="Directory containing PDF source documents (default: ./docs).",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete existing knowledge chunks before indexing. Use for a clean rebuild.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    docs_dir = args.docs_dir.resolve()
    if not docs_dir.is_dir():
        raise SystemExit(f"Documents directory does not exist: {docs_dir}")

    engine = KnowledgeIngestion()
    if args.replace:
        deleted = engine.vector_store.clear()
        print(f"Removed {deleted} existing knowledge chunk(s).")

    count = engine.ingest_folder(docs_dir)
    total = engine.vector_store.count()
    print(f"Indexed {count} chunk(s). Neon now contains {total} searchable chunk(s).")


if __name__ == "__main__":
    main()
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

## scripts/debug_keys.py

**File path:** `scripts/debug_keys.py`

```python

"""Debug script to check Gemini key loading."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from services.llm import LLMManager

print("\n" + "="*60)
print("🔑 DEBUG: Gemini Key Loading")
print("="*60 + "\n")

# Load keys
llm = LLMManager()

print(f"📊 Model: {llm.model_name}")
print(f"📊 Total Keys Found: {len(llm.keys)}")
print(f"📊 Current Key Index: {llm.current_key_index + 1}\n")

print("📋 Key List:")
for i, key in enumerate(llm.keys):
    print(f"  {i+1}. {key[:8]}...{key[-4:]}")

print("\n📊 Key Status:")
status = llm.get_key_status()
for k in status["keys"]:
    print(f"  Key {k['index']}: {k['status']} | Success Rate: {k['success_rate']} | Requests: {k['total_requests']}")

print(f"\n📊 Summary:")
print(f"  Active Keys: {status['summary']['active_keys']}")
print(f"  Available Keys: {status['summary']['available_keys']}")
print(f"  Total Requests: {status['summary']['total_requests']}")

print("\n" + "="*60)
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
"""Test script for KnowledgeAgent."""

from agents.knowledge import KnowledgeAgent
from mao.models.task import Task


def test_knowledge_agent():
    """Test the KnowledgeAgent with a simple query."""
    
    # Create the agent
    agent = KnowledgeAgent()
    
    task = Task(
        name="Knowledge Test",
        description="What should operators do during a pressure spike?",
        assigned_agent="knowledge",
        priority=1,
    )
    
    result = agent.execute(task, context=None)
    
    print("=" * 60)
    print("KnowledgeAgent Test Results")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Confidence: {result.confidence}")
    print(f"Finding: {result.finding}")
    print("\nSummary:")
    print(result.summary)
    print("\nRecommendations:")
    for rec in result.recommendations:
        print(f"  - {rec}")
    print("=" * 60)


if __name__ == "__main__":
    test_knowledge_agent()
```

## scripts/test_mao.py

**File path:** `scripts/test_mao.py`

```python
"""Test script for MAO kernel."""

from mao import MAOKernel
from agents.safety import SafetyAgent
from mao.events.event import Event

# Create kernel
kernel = MAOKernel()

# Register agent
safety = SafetyAgent()
kernel.register_agent(safety)

# Create event
event = Event(
    name="PressureSpike",
    source="SensorAgent",
    payload={
        "asset": "Pump A",
        "pressure": 112,
    },
)

# ✅ FIXED: Use handle_event
report = kernel.handle_event(event)

print("=" * 60)
print("MAO Test Results")
print("=" * 60)
print(f"Workflow: {report.workflow_name}")
print(f"Success: {report.success}")
print(f"Summary: {report.final_summary}")
print(f"Confidence: {report.average_confidence}")
```

## scripts/test_models.py

**File path:** `scripts/test_models.py`

```python
from datetime import datetime
from uuid import uuid4
from models.asset import Asset
from models.enums import AssetStatus, AssetType
from models.sensor import Sensor, SensorType

# ✅ FIXED: Use correct model
sensor = Sensor(
    id=str(uuid4()),
    asset_id="PUMP-001",
    sensor_type=SensorType.PRESSURE,
    value=103.5,
    unit="PSI",
    timestamp=datetime.now(),
)

pump = Asset(
    id="PUMP-001",
    name="Main Feed Pump",
    asset_type=AssetType.PUMP,
    location="Zone A",
    health=98.2,
    status="Running",
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

# ✅ FIXED: Provide path
FAISS_INDEX_PATH = "./data/faiss_index"
store.load(FAISS_INDEX_PATH)

retriever = Retriever(store.db)
results = retriever.retrieve("How do I respond to a pressure spike?")

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content)
```
