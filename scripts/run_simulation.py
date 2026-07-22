import time
from uuid import uuid4

from mao import MAOKernel

from models.asset import Asset, AssetType
from models.facility import Facility

from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator

# Temporary demo classes
<<<<<<< HEAD

from tests.mock_workflow import MockWorkflow
=======
<<<<<<< HEAD
from tests.mock_agent import MockAgent
from tests.mock_workflow import MockWorkflow
=======

from tests.mock_workflow import MockWorkflow
>>>>>>> origin/dev-abeer
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

<<<<<<< HEAD
=======
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer


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
<<<<<<< HEAD
for asset in facility.assets:
    kernel.asset_service.register(asset)

=======
<<<<<<< HEAD
>>>>>>> origin/dev-abeer

kernel.register_workflow(MockWorkflow())
<<<<<<< HEAD
=======
=======
for asset in facility.assets:
    kernel.asset_service.register(asset)


kernel.register_workflow(MockWorkflow())
>>>>>>> origin/dev-abeer
kernel.register_workflow(MockWorkflow())

kernel.register_workflow(PressureWorkflow())
kernel.register_workflow(TemperatureWorkflow())
kernel.register_workflow(GasWorkflow())
kernel.register_workflow(MaintenanceWorkflow())
kernel.register_workflow(FlowWorkflow())
kernel.register_agent(SafetyAgent())
kernel.register_agent(KnowledgeAgent())
kernel.register_agent(MaintenanceAgent())
kernel.register_agent(DiagnosticAgent())
kernel.register_agent(PlanningAgent())

<<<<<<< HEAD
=======
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer

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

<<<<<<< HEAD
    telemetry, reports = simulator.tick(tick)
=======
<<<<<<< HEAD
    telemetry, report = simulator.tick(tick)
=======
    telemetry, reports = simulator.tick(tick)
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer

    print(f"\nTick {tick}")
    print("-" * 50)

    for reading in telemetry:
        print(
            f"{reading.sensor_type.value:<12}"
            f"{reading.value:>8.2f}"
        )

<<<<<<< HEAD
    if reports:
=======
<<<<<<< HEAD
    if report:
>>>>>>> origin/dev-abeer
        print("\n🚨 INCIDENT DETECTED")

<<<<<<< HEAD
        for report in reports:
            print(report.final_summary)
=======
=======
    if reports:
        print("\n🚨 INCIDENT DETECTED")

        for report in reports:
            print(report.final_summary)
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer
    


    time.sleep(1)
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
>>>>>>> origin/dev-abeer
    print("\nRegistered Agents")

    for agent in kernel.registry.all():
        print("-", agent.name)
<<<<<<< HEAD
=======
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer

    print("\nTelemetry History")

    for asset in facility.assets:

        history = kernel.state.get_history(asset.id)

        print(
        f"{asset.name:<10} -> {len(history)} readings"
    )
    print("\nAsset Health")

    for asset in facility.assets:

        history = kernel.state.get_history(asset.id)

<<<<<<< HEAD
        # Calculate current health
=======
<<<<<<< HEAD
>>>>>>> origin/dev-abeer
        health = kernel.health.calculate_health(history)

        # Update the asset in the AssetService
        kernel.asset_service.update_health(asset.id, health)

        # Fetch the Asset object
        asset_obj = kernel.asset_service.get(asset.id)

        print(
<<<<<<< HEAD
=======
            f"{asset.name:<10} {health:.1f}%"
        )
=======
        # Calculate current health
        health = kernel.health.calculate_health(history)

        # Update the asset in the AssetService
        kernel.asset_service.update_health(asset.id, health)

        # Fetch the Asset object
        asset_obj = kernel.asset_service.get(asset.id)

        print(
>>>>>>> origin/dev-abeer
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
<<<<<<< HEAD
    )
=======
    )
>>>>>>> origin/dev-ashutosh-zinia
>>>>>>> origin/dev-abeer
