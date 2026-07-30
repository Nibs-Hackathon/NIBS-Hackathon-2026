"""Generate multiple refineries with hundreds of assets."""

from typing import List, Dict
from models.asset import Asset, AssetType, Refinery
from uuid import NAMESPACE_URL, uuid5
import random


class RefineryGenerator:
    """Generate realistic refinery assets for simulation."""

    REFINERY_NAMES = [
        "RigOS Alpha Refinery",
        "North Terminal Refinery",
        "South Coast Refinery",
        "East Valley Refinery",
        "West Port Refinery",
        "Central Hub Refinery",
        "Gulf Coast Refinery",
        "Pacific Refinery",
        "Atlantic Refinery",
        "Midwest Refinery",
        "Mumbai Coastal Refinery",
        "Jamnagar Energy Refinery",
        "Paradip Eastern Refinery",
        "Chennai South Refinery",
        "Colombo Gateway Refinery",
        "Chattogram Bay Refinery",
    ]

    ZONES = ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E", "Zone F"]

    PUMP_NAMES = ["Pump A", "Pump B", "Pump C", "Pump D", "Pump E", "Pump F", "Pump G", "Pump H"]
    COMPRESSOR_NAMES = ["Compressor C-01", "Compressor C-02", "Compressor C-03", "Compressor C-04"]
    VALVE_NAMES = ["Valve V-01", "Valve V-02", "Valve V-03", "Valve V-04", "Valve V-05"]
    HEAT_EXCHANGER_NAMES = ["HX-01", "HX-02", "HX-03", "HX-04"]
    TANK_NAMES = ["Tank T-01", "Tank T-02", "Tank T-03", "Tank T-04"]
    REACTOR_NAMES = ["Reactor R-01", "Reactor R-02"]
    PIPELINE_NAMES = ["Pipeline P-01", "Pipeline P-02", "Pipeline P-03"]

    @staticmethod
    def _stable_id(kind: str, *parts: str) -> str:
        """Keep facility and asset lineage stable across process restarts."""
        key = ":".join(str(part) for part in parts)
        return str(uuid5(NAMESPACE_URL, f"rigos:{kind}:{key}"))

    @classmethod
    def generate_assets_for_refinery(
        cls,
        refinery_name: str,
        asset_count: int = 50,
        refinery_id: str | None = None,
    ) -> List[Asset]:
        """Generate assets for a refinery."""
        assets = []
        refinery_id = refinery_id or cls._stable_id("refinery", refinery_name)
        rng = random.Random(refinery_id)

        # Determine how many of each type
        pumps = asset_count // 5
        compressors = asset_count // 10
        valves = asset_count // 8
        heat_exchangers = asset_count // 12
        tanks = asset_count // 15
        reactors = asset_count // 20
        pipelines = asset_count // 15
        others = asset_count - (pumps + compressors + valves + heat_exchangers + tanks + reactors + pipelines)

        # Generate Pumps
        for i in range(pumps):
            name = f"Pump {chr(65 + i % 26)}-{i // 26 + 1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.PUMP,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=rng.choice(cls.ZONES),
                health=rng.uniform(70, 100),
                status=rng.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Compressors
        for i in range(compressors):
            name = f"Compressor C-{i+1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.COMPRESSOR,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=rng.choice(cls.ZONES),
                health=rng.uniform(65, 98),
                status=rng.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.6, 0.25, 0.1, 0.05])[0],
            ))

        # Generate Valves
        for i in range(valves):
            name = f"Valve V-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.VALVE,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=rng.choice(cls.ZONES),
                health=rng.uniform(60, 100),
                status=rng.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.65, 0.25, 0.08, 0.02])[0],
            ))

        # Generate Heat Exchangers
        for i in range(heat_exchangers):
            name = f"HX-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.HEAT_EXCHANGER,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=rng.choice(cls.ZONES),
                health=rng.uniform(50, 95),
                status=rng.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.5, 0.25, 0.15, 0.1])[0],
            ))

        # Generate Tanks
        for i in range(tanks):
            name = f"Tank T-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.TANK,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=rng.choice(cls.ZONES),
                health=rng.uniform(70, 100),
                status=rng.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Reactors
        for i in range(reactors):
            name = f"Reactor R-{i+1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.REACTOR,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=rng.choice(cls.ZONES),
                health=rng.uniform(60, 95),
                status=rng.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.55, 0.25, 0.15, 0.05])[0],
            ))

        # Generate Pipelines
        for i in range(pipelines):
            name = f"Pipeline P-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.PIPELINE,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=rng.choice(cls.ZONES),
                health=rng.uniform(65, 100),
                status=rng.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Other assets
        other_types = [AssetType.MOTOR, AssetType.GENERATOR, AssetType.BOILER, AssetType.TURBINE, AssetType.DISTILLATION_COLUMN]
        for i in range(others):
            asset_type = rng.choice(other_types)
            name = f"{asset_type.value} {i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=asset_type,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=rng.choice(cls.ZONES),
                health=rng.uniform(60, 98),
                status=rng.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.6, 0.25, 0.1, 0.05])[0],
            ))

        for asset in assets:
            asset.id = cls._stable_id("asset", refinery_id, asset.name)
        return assets

    @classmethod
    def generate_refineries(cls, count: int = 5, assets_per_refinery: int = 50) -> List[Refinery]:
        """Generate multiple refineries with assets."""
        refineries = []
        selected_names = cls.REFINERY_NAMES[:min(count, len(cls.REFINERY_NAMES))]

        for name in selected_names:
            refinery_id = cls._stable_id("refinery", name)
            assets = cls.generate_assets_for_refinery(
                name,
                assets_per_refinery,
                refinery_id=refinery_id,
            )
            try:
                from services.refinery_geo import REFINERY_GEO, format_display_location
                location = format_display_location(REFINERY_GEO.get(name)) or name
            except Exception:
                location = name
            refineries.append(Refinery(
                id=refinery_id,
                name=name,
                location=location,
                assets=assets,
                status=random.Random(refinery_id).choices(["Active", "Active", "Active", "Maintenance"])[0],
            ))

        return refineries
