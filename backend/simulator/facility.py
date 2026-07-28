from models.facility import Facility
from simulator.asset import SimulatedAsset


class SimulatedFacility:
    def __init__(self, facility: Facility):
        self.assets = [SimulatedAsset(asset) for asset in facility.assets]
        self.active_faults = {}

    def tick(self, tick_number, fault=None, target_asset_id=None):
        """Generate telemetry with an optional targeted, time-limited fault."""
        telemetry = []

        for asset in self.assets:
            current_fault = None
            asset_id = asset.asset.id

            if target_asset_id and asset_id == target_asset_id and fault:
                current_fault = fault
                self.active_faults[asset_id] = {
                    "sensor": fault.get("sensor"),
                    "value": fault.get("value"),
                    "ticks_remaining": 8,
                    "active": True,
                }
            elif asset_id in self.active_faults:
                fault_data = self.active_faults[asset_id]
                ticks_remaining = int(fault_data.get("ticks_remaining", 0))
                if fault_data.get("active") and ticks_remaining > 0:
                    current_fault = {
                        "sensor": fault_data.get("sensor"),
                        "value": fault_data.get("value"),
                    }
                    fault_data["ticks_remaining"] = ticks_remaining - 1
                else:
                    fault_data["active"] = False

            telemetry.extend(asset.tick(fault=current_fault))

        return telemetry
