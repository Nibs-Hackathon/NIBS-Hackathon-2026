import streamlit as st
from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_asset_detail_panel
from ui_helpers import asset_monitor_demo_snapshot, metric_card, page_heading, render_sidebar, setup_page, trend_series

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")
page_heading("FLEET INTELLIGENCE", "Asset Monitoring", "Health, telemetry, and operational posture for every connected asset.")
render_live_signal_banner("ASSET DEMO SNAPSHOT", "The existing asset and telemetry demo is isolated for future state-manager integration.", "Info")
st.write("")

snapshot = asset_monitor_demo_snapshot()
assets = snapshot["assets"]
filters = st.columns(3)
with filters[0]: zone = st.selectbox("Zone", ["All zones", "Process A", "Process B", "Terminal", "Pipeline", "Utilities"])
with filters[1]: status = st.selectbox("Status", ["All statuses", "Healthy", "Warning", "Critical"])
with filters[2]: selected = st.selectbox("Focus asset", [a["Asset"] for a in assets])

# TODO: Replace asset_monitor_demo_snapshot with a read-only asset/telemetry adapter.
visible = [a for a in assets if (zone == "All zones" or a["Zone"] == zone) and (status == "All statuses" or a["Status"] == status)]
st.dataframe(visible, hide_index=True, use_container_width=True, height=260)

st.write("")
for col, args in zip(st.columns(4), [("Selected asset", selected, "Telemetry connected", "cyan"), ("Current health", "82%", "Watch threshold: 80%", "amber"), ("Sensor coverage", "5 / 5", "All channels reporting", "green"), ("Last update", "18 sec", "Within SLA", "green")]):
    with col: metric_card(*args)

left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>HEALTH & SAFETY TREND</div>", unsafe_allow_html=True)
    st.line_chart(trend_series(18, 84, 8), color=["#55D6FF", "#4FE3B2"], height=260)
with right:
    selected_asset = next(asset for asset in assets if asset["Asset"] == selected)
    render_asset_detail_panel(selected_asset, snapshot["sensors"])
