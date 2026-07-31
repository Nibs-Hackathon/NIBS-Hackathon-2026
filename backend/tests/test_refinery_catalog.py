from services.refinery_generator import RefineryGenerator
from services.refinery_geo import REFINERY_GEO


def test_every_generated_refinery_has_geo_metadata():
    assert set(RefineryGenerator.REFINERY_NAMES) == set(REFINERY_GEO)


def test_india_region_catalog_is_present():
    india_sites = {
        name for name, geo in REFINERY_GEO.items()
        if geo.get("country") == "India"
    }

    assert india_sites == {
        "Mumbai Coastal Refinery",
        "Jamnagar Energy Refinery",
        "Paradip Eastern Refinery",
        "Chennai South Refinery",
    }


def test_assets_share_their_parent_refinery_id():
    refinery = RefineryGenerator.generate_refineries(count=1, assets_per_refinery=12)[0]

    assert refinery.assets
    assert all(asset.refinery_id == refinery.id for asset in refinery.assets)


def test_full_portfolio_has_a_distinct_asset_profile_per_facility():
    refineries = RefineryGenerator.generate_refineries(
        count=len(RefineryGenerator.REFINERY_NAMES),
        assets_per_refinery=24,
    )

    assert len(refineries) == len(RefineryGenerator.REFINERY_NAMES)
    assert all(len(refinery.assets) == 24 for refinery in refineries)
    assert len({asset.id for refinery in refineries for asset in refinery.assets}) == 24 * len(refineries)


def test_facility_and_asset_ids_are_stable_across_restarts():
    first = RefineryGenerator.generate_assets_for_refinery("Midwest Refinery", asset_count=12)
    second = RefineryGenerator.generate_assets_for_refinery("Midwest Refinery", asset_count=12)

    assert [asset.refinery_id for asset in first] == [asset.refinery_id for asset in second]
    assert [asset.id for asset in first] == [asset.id for asset in second]
