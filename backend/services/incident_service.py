"""Manual incident injection for the shared live simulator."""

import time

from models.sensor import SensorType


class IncidentService:
    """Inject operator-requested faults into the shared live simulator."""

    FAULTS = {
        "pressure spike": {"sensor": SensorType.PRESSURE, "value": 155},
        "gas leak": {"sensor": SensorType.GAS, "value": 30},
        "high vibration": {"sensor": SensorType.VIBRATION, "value": 40},
        "high temperature": {"sensor": SensorType.TEMPERATURE, "value": 95},
        "flow restriction": {"sensor": SensorType.FLOW, "value": 15},
    }

    def __init__(self, simulator):
        self.simulator = simulator

    def trigger_incident(self, incident_type):
        normalized_type = " ".join(
            incident_type.strip().lower().replace("_", " ").replace("-", " ").split()
        )
        fault = self.FAULTS.get(normalized_type)
        if fault is None:
            supported = ", ".join(sorted(self.FAULTS))
            raise ValueError(f"Unsupported incident type. Choose one of: {supported}")

        active_assets = getattr(self.simulator, "active_incidents", {})
        target = next(
            (
                simulated_asset
                for simulated_asset in self.simulator.facility.assets
                if simulated_asset.asset.id not in active_assets
            ),
            None,
        )
        if target is None:
            raise RuntimeError("No asset is currently available for fault injection.")

        telemetry, reports = self.simulator.tick(
            tick_number=int(time.time()),
            fault=fault,
            target_asset_id=target.asset.id,
        )

        return {
            "incident_type": normalized_type,
            "asset_id": target.asset.id,
            "telemetry_count": len(telemetry),
            "reports_count": len(reports),
        }
