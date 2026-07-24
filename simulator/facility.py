from models.facility import Facility
from simulator.asset import SimulatedAsset
from models.sensor import SensorType


class SimulatedFacility:
    def __init__(self, facility: Facility):
        self.assets = [
            SimulatedAsset(asset)
            for asset in facility.assets
        ]
        self.active_faults = {}

    def tick(self, tick_number, fault=None, target_asset_id=None):
        """Generate telemetry with optional targeted fault."""
        telemetry = []
        
        for asset in self.assets:
            current_fault = None
            
            # ✅ Check if this asset has an active fault
            if target_asset_id and asset.asset.id == target_asset_id:
                if fault:
                    current_fault = fault
                    self.active_faults[asset.asset.id] = {
                        "sensor": fault.get("sensor"),
                        "value": fault.get("value"),
                        "tick": tick_number,
                        "active": True
                    }
            elif asset.asset.id in self.active_faults:
                fault_data = self.active_faults[asset.asset.id]
                if fault_data.get("active", False):
                    ticks_active = tick_number - fault_data.get("tick", tick_number)
                    # ✅ Fault lasts 5 ticks then auto-resolves
                    if ticks_active > 5:
                        fault_data["active"] = False
                        print(f"✅ Fault resolved for {asset.asset.name} after {ticks_active} ticks")
                    else:
                        current_fault = {
                            "sensor": fault_data.get("sensor"),
                            "value": fault_data.get("value")
                        }
            
            telemetry.extend(asset.tick(fault=current_fault))
        
        return telemetry