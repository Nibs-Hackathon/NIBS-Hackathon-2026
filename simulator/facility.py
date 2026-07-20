from models.facility import Facility
from simulator.asset import SimulatedAsset


class SimulatedFacility:

    def __init__(self, facility: Facility):

        self.assets = [
            SimulatedAsset(asset)
            for asset in facility.assets
        ]

    def tick(self, tick_number: int):

        telemetry = []

        for index, asset in enumerate(self.assets):

            # Inject a pressure spike into Pump A on tick 10
            inject_fault = (
                index == 0 and tick_number == 10
            )

            telemetry.extend(
                asset.tick(
                    inject_fault=inject_fault
                )
            )

        return telemetry