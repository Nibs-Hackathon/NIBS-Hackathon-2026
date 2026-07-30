"""Static geographic metadata for refinery names (keyed by asset.location)."""

from __future__ import annotations

from typing import Any

REFINERY_GEO: dict[str, dict[str, Any]] = {
    "RigOS Alpha Refinery": {
        "country": "United States",
        "state": "Texas",
        "sea": "Gulf of Mexico",
        "lat": 29.76,
        "lng": -95.37,
    },
    "North Terminal Refinery": {
        "country": "Norway",
        "state": "Rogaland",
        "sea": "North Sea",
        "lat": 58.97,
        "lng": 5.73,
    },
    "South Coast Refinery": {
        "country": "United States",
        "state": "Louisiana",
        "sea": "Gulf of Mexico",
        "lat": 29.95,
        "lng": -90.07,
    },
    "East Valley Refinery": {
        "country": "United Arab Emirates",
        "state": "Abu Dhabi",
        "sea": "Persian Gulf",
        "lat": 24.45,
        "lng": 54.37,
    },
    "West Port Refinery": {
        "country": "United States",
        "state": "California",
        "sea": "Pacific Ocean",
        "lat": 33.75,
        "lng": -118.27,
    },
    "Central Hub Refinery": {
        "country": "United States",
        "state": "Oklahoma",
        "sea": "Midcontinent pipeline hub",
        "lat": 35.47,
        "lng": -97.52,
    },
    "Gulf Coast Refinery": {
        "country": "United States",
        "state": "Texas",
        "sea": "Gulf of Mexico",
        "lat": 29.30,
        "lng": -94.80,
    },
    "Pacific Refinery": {
        "country": "Singapore",
        "state": "Jurong Island",
        "sea": "Singapore Strait",
        "lat": 1.26,
        "lng": 103.82,
    },
    "Atlantic Refinery": {
        "country": "United States",
        "state": "New Jersey",
        "sea": "Atlantic Ocean",
        "lat": 40.72,
        "lng": -74.17,
    },
    "Midwest Refinery": {
        "country": "United States",
        "state": "Illinois",
        "sea": "Lake Michigan",
        "lat": 41.88,
        "lng": -87.63,
    },
    "Mumbai Coastal Refinery": {
        "country": "India",
        "state": "Maharashtra",
        "sea": "Arabian Sea",
        "lat": 19.02,
        "lng": 72.84,
    },
    "Jamnagar Energy Refinery": {
        "country": "India",
        "state": "Gujarat",
        "sea": "Gulf of Kutch",
        "lat": 22.47,
        "lng": 70.07,
    },
    "Paradip Eastern Refinery": {
        "country": "India",
        "state": "Odisha",
        "sea": "Bay of Bengal",
        "lat": 20.32,
        "lng": 86.61,
    },
    "Chennai South Refinery": {
        "country": "India",
        "state": "Tamil Nadu",
        "sea": "Bay of Bengal",
        "lat": 13.10,
        "lng": 80.29,
    },
    "Colombo Gateway Refinery": {
        "country": "Sri Lanka",
        "state": "Western Province",
        "sea": "Indian Ocean",
        "lat": 6.95,
        "lng": 79.84,
    },
    "Chattogram Bay Refinery": {
        "country": "Bangladesh",
        "state": "Chattogram",
        "sea": "Bay of Bengal",
        "lat": 22.35,
        "lng": 91.78,
    },
}


def format_display_location(geo: dict[str, Any] | None) -> str | None:
    if not geo:
        return None
    state = geo.get("state")
    country = geo.get("country")
    sea = geo.get("sea")
    region = ", ".join(part for part in (state, country) if part)
    if region and sea:
        return f"{region} · {sea}"
    return region or sea


def refinery_geo_payload(refinery_name: str) -> dict[str, Any]:
    """Flatten geo fields for operations snapshot refinery rows."""
    geo = REFINERY_GEO.get(refinery_name)
    if not geo:
        return {}
    return {
        **geo,
        "display_location": format_display_location(geo),
    }


# ponytail: catalog must cover every generator name or globe/switcher miss sites
from services.refinery_generator import RefineryGenerator

assert all(name in REFINERY_GEO for name in RefineryGenerator.REFINERY_NAMES)
