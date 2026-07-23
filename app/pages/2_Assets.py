import streamlit as st

from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_asset_detail_panel

from ui_helpers import (
    metric_card,
    page_heading,
    render_sidebar,
    setup_page,
)

from frontend_services.asset_adapter import get_assets
from frontend_services.telemetry_adapter import get_asset_telemetry
from frontend_services.health_adapter import get_asset_health


# -------------------------
# Setup
# -------------------------

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")

page_heading(
    "FLEET INTELLIGENCE",
    "Asset Monitoring",
    "Health, telemetry, and operational posture for every connected asset."
)


render_live_signal_banner(
    "LIVE ASSET TELEMETRY",
    "Connected to RigOS backend state manager.",
    "Info"
)

st.write("")


# -------------------------
# Load assets
# -------------------------

snapshot = get_assets()

assets = snapshot["assets"]


if not assets:
    st.warning("No assets available.")
    st.stop()


# -------------------------
# Filters
# -------------------------

filters = st.columns(3)


with filters[0]:

    zones = [
        "All zones"
    ] + list(
        set(
            asset["Zone"]
            for asset in assets
        )
    )

    zone = st.selectbox(
        "Zone",
        zones
    )


with filters[1]:

    statuses = [
        "All statuses"
    ] + list(
        set(
            asset["Status"]
            for asset in assets
        )
    )

    status = st.selectbox(
        "Status",
        statuses
    )


with filters[2]:

    selected = st.selectbox(
        "Focus asset",
        [
            asset["Asset"]
            for asset in assets
        ]
    )


# -------------------------
# Filtered assets
# -------------------------

visible = [
    asset
    for asset in assets
    if (
        zone == "All zones"
        or asset["Zone"] == zone
    )
    and (
        status == "All statuses"
        or asset["Status"] == status
    )
]


st.dataframe(
    visible,
    hide_index=True,
    use_container_width=True,
    height=260
)


# -------------------------
# Selected asset
# -------------------------

selected_asset = next(
    asset
    for asset in assets
    if asset["Asset"] == selected
)


asset_id = selected_asset["id"]


# -------------------------
# Backend data
# -------------------------

health_data = get_asset_health(
    asset_id
)

telemetry_data = get_asset_telemetry(
    asset_id
)


# -------------------------
# Metrics
# -------------------------

health = health_data["health"]

health_status = (
    "Healthy"
    if health >= 80
    else "Warning"
)


latest = telemetry_data["latest"]


sensor_count = (
    len(snapshot["sensors"])
    if "sensors" in snapshot
    else 0
)


last_update = (
    latest["Timestamp"]
    if latest
    else "No telemetry"
)


metrics = [
    (
        "Selected asset",
        selected,
        "Telemetry connected",
        "cyan"
    ),
    (
        "Current health",
        f"{health}%",
        health_status,
        "green"
    ),
    (
        "Sensor coverage",
        f"{sensor_count}",
        "channels reporting",
        "green"
    ),
    (
        "Last update",
        str(last_update),
        "Backend state",
        "green"
    )
]


for col, args in zip(
    st.columns(4),
    metrics
):

    with col:
        metric_card(*args)


# -------------------------
# Trend + Detail
# -------------------------

left, right = st.columns(
    [1.55, 1]
)


with left:

    st.markdown(
        "<div class='section-label'>HEALTH & SAFETY TREND</div>",
        unsafe_allow_html=True
    )


    history = telemetry_data["history"]


    if history:

        st.line_chart(
            history,
            height=260
        )

    else:

        st.info(
            "No telemetry history available yet."
        )


with right:

    render_asset_detail_panel(
        selected_asset,
        snapshot["sensors"]
    )