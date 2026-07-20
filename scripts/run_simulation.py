import time
from uuid import uuid4

from mao import MAOKernel

from models.asset import Asset, AssetType
from models.facility import Facility

from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator

# Temporary demo classes
from tests.mock_agent import MockAgent
from tests.mock_workflow import MockWorkflow


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

kernel.register_agent(MockAgent())
kernel.register_workflow(MockWorkflow())

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

    telemetry, report = simulator.tick(tick)

    print(f"\nTick {tick}")
    print("-" * 50)

    for reading in telemetry:
        print(
            f"{reading.sensor_type.value:<12}"
            f"{reading.value:>8.2f}"
        )

    if report:
        print("\n🚨 INCIDENT DETECTED")
        print(report.final_summary)

    


    time.sleep(1)

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

        print(
            f"{asset.name:<10} {health:.1f}%"
        )