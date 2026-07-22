from mao import MAOKernel

from models.asset import Asset, AssetType
from models.facility import Facility

from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator



kernel = MAOKernel()


assets = [

    Asset(
        name="Pump A-01",
        asset_type=AssetType.PUMP,
        location="Zone A"
    ),

]


facility = Facility(
    id="rigos-alpha",
    name="RigOS Alpha",
    assets=assets
)


for asset in assets:

    kernel.asset_service.register(asset)



simulated_facility = SimulatedFacility(
    facility
)


simulator = Simulator(
    facility=simulated_facility,
    kernel=kernel
)