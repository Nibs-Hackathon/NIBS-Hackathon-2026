import streamlit as st
from components.phase_one_views import render_live_signal_banner
from ui_helpers import (
    metric_card,
    page_heading,
    render_health_heatmap,
    render_sidebar,
    setup_page
)

from frontend_services.dashboard_adapter import get_dashboard

setup_page("Dashboard")
render_sidebar("Executive Dashboard")
page_heading("OVERVIEW", "Operations Dashboard", "Real-time operational intelligence across the facility.")
snapshot = get_dashboard()
render_live_signal_banner("LIVE DEMO TELEMETRY", "Operational data shown is the existing frontend demo snapshot. Backend stream integration is pending.")
st.write("")

for col, args in zip(st.columns(4), snapshot["metrics"]):
    with col: metric_card(*args)

st.write("")
st.markdown("<div class='section-label'>FACILITY HEALTH HEATMAP</div>", unsafe_allow_html=True)
render_health_heatmap()
st.write("")
left, right = st.columns([1.65, 1])
with left:
    st.markdown("<div class='section-label'>24-HOUR OPERATIONAL HEALTH</div>", unsafe_allow_html=True)
    st.info(
        "Live health trend will appear after telemetry history is populated."
    )
with right:
    st.markdown("<div class='section-label'>ATTENTION QUEUE</div>", unsafe_allow_html=True)
    for item in snapshot["incidents"]:
        st.markdown(f"<div class='panel'><b>{item['Incident']}</b><br><span class='muted'>{item['Asset']} • {item['Severity']} • {item['Detected']}</span></div>", unsafe_allow_html=True)
        st.write("")

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>ASSET WATCHLIST</div>", unsafe_allow_html=True)
    st.dataframe(snapshot["assets"], hide_index=True, use_container_width=True, height=245)
with right:
    st.markdown("<div class='section-label'>LIVE ACTIVITY</div>", unsafe_allow_html=True)
    for time, actor, text in snapshot["activity"]:
        st.markdown(f"**{time} · {actor}**  \n<span class='muted'>{text}</span>", unsafe_allow_html=True)
