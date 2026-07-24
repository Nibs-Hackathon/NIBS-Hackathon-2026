import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from components.phase_one_views import render_live_signal_banner
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page
from frontend_services.asset_adapter import get_assets
from frontend_services.telemetry_adapter import get_asset_telemetry
from frontend_services.health_adapter import get_asset_health

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")
page_heading("FLEET INTELLIGENCE", "Asset Monitoring", "Health, telemetry, and operational posture for every connected asset.")

render_live_signal_banner("LIVE ASSET TELEMETRY", "Connected to RigOS backend state manager.", "Info")
st.write("")

snapshot = get_assets()
assets = snapshot.get("assets", [])

if not assets:
    st.warning("No assets available. Start the simulation to see assets.")
    st.stop()

# Filters
filters = st.columns(3)
with filters[0]:
    zones = ["All zones"] + list(set(a.get("location", "Unknown") for a in assets))
    zone = st.selectbox("Zone", zones)

with filters[1]:
    statuses = ["All statuses"] + list(set(a.get("status", "Unknown") for a in assets))
    status = st.selectbox("Status", statuses)

with filters[2]:
    selected = st.selectbox("Focus asset", [a.get("name", "Unknown") for a in assets])

# Filtered assets
visible = [
    a for a in assets
    if (zone == "All zones" or a.get("location") == zone)
    and (status == "All statuses" or a.get("status") == status)
]

st.dataframe(visible, hide_index=True, use_container_width=True, height=260)

# Selected asset
selected_asset = next((a for a in assets if a.get("name") == selected), assets[0])
asset_id = selected_asset.get("id")

if asset_id:
    health_data = get_asset_health(asset_id)
    telemetry_data = get_asset_telemetry(asset_id)
    
    health = health_data.get("health", 0)
    latest = telemetry_data.get("latest", {})
    
    metrics = [
        ("Selected asset", selected, "Telemetry connected", "cyan"),
        ("Current health", f"{health:.1f}%", "Healthy" if health >= 80 else "Warning", "green"),
        ("Sensor coverage", "4", "channels reporting", "green"),
        ("Last update", str(latest.get("timestamp", "No data")), "Backend state", "green"),
    ]
    
    for col, args in zip(st.columns(4), metrics):
        with col:
            metric_card(*args)
    
    left, right = st.columns([1.55, 1])
    with left:
        st.markdown("<div class='section-label'>HEALTH & SAFETY TREND</div>", unsafe_allow_html=True)
        history = telemetry_data.get("history", [])
        if history:
            st.line_chart(history, height=260)
        else:
            st.info("No telemetry history available yet.")
    
    with right:
        from components.phase_two_views import render_asset_detail_panel
        sensors = snapshot.get("sensors", [])
        render_asset_detail_panel(selected_asset, sensors)