import importlib

import streamlit as st
import ui_helpers

# Refresh shared UI helpers during Streamlit development reruns so an older
# module cached by the script runner cannot mask newly added components.
importlib.reload(ui_helpers)

from ui_helpers import executive_metrics, metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Operations Center")
render_sidebar("Operations Center")
page_heading("NIBS / AI OPERATIONS CENTER", "Welcome to Command Nexus", "A unified mission-control surface for operational intelligence, risk, and response.")

left, right = st.columns([1.45, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>MISSION STATUS</div><h3 style='margin:.2rem 0 .6rem'>Operational picture: stable, with two monitored assets.</h3><p class='muted'>Use the dashboard to review live health, incidents, agent decisions, and the current response queue.</p></div>", unsafe_allow_html=True)
with right:
    st.markdown(f"<div class='panel'><div class='section-label'>PLATFORM STATUS</div>{status_chip('Running')}<p class='muted' style='margin-top:.8rem'>Demo workspace • Simulated telemetry</p></div>", unsafe_allow_html=True)

st.write("")
st.markdown("<div class='section-label'>EXECUTIVE MISSION CONTROL</div>", unsafe_allow_html=True)
for metric_row in [executive_metrics()[:4], executive_metrics()[4:]]:
    for col, args in zip(st.columns(4), metric_row):
        with col:
            metric_card(*args)

st.write("")
st.markdown("<div class='panel'><div class='section-label'>QUICK START</div><p class='muted'>Navigate with the sidebar to inspect assets, simulate an incident, ask the global copilot, inspect predictive health, or review AI activity.</p></div>", unsafe_allow_html=True)
