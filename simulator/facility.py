from models.facility import Facility
from simulator.asset import SimulatedAsset
from simulator.fault_injector import FaultInjector
from models.sensor import SensorType


class SimulatedFacility:

    def __init__(self, facility: Facility):

        self.assets = [
            SimulatedAsset(asset)
            for asset in facility.assets
        ]

        self.injector = FaultInjector()

        self.injector.schedule(
            tick=10,
            asset_index=0,
            sensor=SensorType.PRESSURE,
            value=155,
        )

        self.injector.schedule(
            tick=20,
            asset_index=1,
            sensor=SensorType.TEMPERATURE,
            value=95,
        )

        self.injector.schedule(
            tick=30,
            asset_index=2,
            sensor=SensorType.GAS,
            value=35,
        )

        self.injector.schedule(
            tick=40,
            asset_index=0,
            sensor=SensorType.VIBRATION,
            value=40,
        )

        self.injector.schedule(
            tick=50,
            asset_index=1,
            sensor=SensorType.FLOW,
            value=15,
        )

    def tick(self, tick_number, fault=None):

        telemetry = []

        for index, asset in enumerate(self.assets):

            if fault and index == 0:
                fault=  fault
            else:
                fault = self.injector.get_fault(
                    tick_number,
                    index
                )

            telemetry.extend(
                asset.tick(
                    asset_fault=fault
                )
            )

        return telemetry