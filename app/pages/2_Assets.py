import streamlit as st
from ui_helpers import metric_card, mock_assets, page_heading, render_sidebar, setup_page, trend_series

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")
page_heading("FLEET INTELLIGENCE", "Asset Monitoring", "Health, telemetry, and operational posture for every connected asset.")

assets = mock_assets()
filters = st.columns(3)
with filters[0]: zone = st.selectbox("Zone", ["All zones", "Process A", "Process B", "Terminal", "Pipeline", "Utilities"])
with filters[1]: status = st.selectbox("Status", ["All statuses", "Healthy", "Warning", "Critical"])
with filters[2]: selected = st.selectbox("Focus asset", [a["Asset"] for a in assets])

# TODO: Replace mock_assets with AssetService/state-manager data once a UI data interface is exposed.
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
    st.markdown("<div class='section-label'>SENSOR SNAPSHOT</div>", unsafe_allow_html=True)
    st.dataframe([{"Sensor": "Pressure", "Reading": "119.4 bar", "State": "Normal"}, {"Sensor": "Temperature", "Reading": "76.2 °C", "State": "Normal"}, {"Sensor": "Vibration", "Reading": "23.7 mm/s", "State": "Watch"}, {"Sensor": "Flow", "Reading": "63.1 m³/h", "State": "Normal"}], hide_index=True, use_container_width=True)
