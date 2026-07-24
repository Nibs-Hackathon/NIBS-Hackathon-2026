import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from components.phase_one_views import render_live_signal_banner
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page
from app.frontend_services.backend_api_new import api

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")
page_heading("FLEET INTELLIGENCE", "Asset Monitoring", "Health, telemetry, and operational posture for every connected asset.")

render_live_signal_banner("LIVE ASSET TELEMETRY", "Connected to RigOS backend state manager.", "Info")
st.write("")

# -------------------------
# Refinery Selector
# -------------------------

refineries = api.get_refineries()

if not refineries:
    st.warning("No refineries available. Start the simulation to see assets.")
    st.stop()

# Refinery selection
refinery_names = [r["name"] for r in refineries]
selected_refinery_name = st.selectbox("🏭 Select Refinery", refinery_names)
selected_refinery = next(r for r in refineries if r["name"] == selected_refinery_name)

# Get assets for this refinery
all_assets = selected_refinery["assets"]
refinery_id = selected_refinery["id"]

st.markdown(f"**{selected_refinery_name}** - {selected_refinery['location']} | **{len(all_assets)}** assets")

# -------------------------
# Filters
# -------------------------

filters = st.columns(4)

with filters[0]:
    asset_types = ["All Types"] + sorted(set(a["type"] for a in all_assets))
    selected_type = st.selectbox("Asset Type", asset_types)

with filters[1]:
    zones = ["All Zones"] + sorted(set(a.get("zone", "Unassigned") for a in all_assets))
    selected_zone = st.selectbox("Zone", zones)

with filters[2]:
    statuses = ["All Statuses"] + sorted(set(a["status"] for a in all_assets))
    selected_status = st.selectbox("Status", statuses)

with filters[3]:
    # Health range filter
    health_min = st.slider("Min Health %", 0, 100, 0)

# Filter assets
visible = [
    a for a in all_assets
    if (selected_type == "All Types" or a["type"] == selected_type)
    and (selected_zone == "All Zones" or a.get("zone", "Unassigned") == selected_zone)
    and (selected_status == "All Statuses" or a["status"] == selected_status)
    and (a["health"] >= health_min)
]

st.dataframe(visible, hide_index=True, use_container_width=True, height=300)
st.caption(f"Showing {len(visible)} of {len(all_assets)} assets")

# -------------------------
# Asset Type Distribution
# -------------------------

st.markdown("### 📊 Asset Distribution")

# Count by type
type_counts = {}
for a in all_assets:
    t = a["type"]
    type_counts[t] = type_counts.get(t, 0) + 1

# Display as metrics
cols = st.columns(min(len(type_counts), 8))
for i, (asset_type, count) in enumerate(sorted(type_counts.items())):
    with cols[i % len(cols)]:
        st.metric(asset_type, count)

# -------------------------
# Selected Asset Detail
# -------------------------

if visible:
    st.markdown("### 🔍 Asset Detail")

    # Select an asset to inspect
    asset_names = [a["name"] for a in visible]
    selected_name = st.selectbox("Select asset to inspect", asset_names)
    selected_asset = next(a for a in visible if a["name"] == selected_name)

    # Display asset details
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Name", selected_asset["name"])
    with col2:
        st.metric("Type", selected_asset["type"])
    with col3:
        st.metric("Health", f"{selected_asset['health']:.1f}%")
    with col4:
        st.metric("Status", selected_asset["status"])

    # Get telemetry for this asset
    try:
        from frontend_services.telemetry_adapter import get_asset_telemetry
        telemetry = get_asset_telemetry(selected_asset["id"])
        if telemetry and telemetry.get("history"):
            st.line_chart(telemetry["history"], height=200)
        else:
            st.info("No telemetry history available for this asset. Run the simulation.")
    except Exception as e:
        st.info("Telemetry data not available.")