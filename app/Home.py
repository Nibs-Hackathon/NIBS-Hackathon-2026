import streamlit as st

from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Operations Center")
render_sidebar("Operations Center")
page_heading("NIBS / AI OPERATIONS CENTER", "Welcome to Command Nexus", "A unified mission-control surface for operational intelligence, risk, and response.")

left, right = st.columns([1.45, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>MISSION STATUS</div><h3 style='margin:.2rem 0 .6rem'>Operational picture: stable, with two monitored assets.</h3><p class='muted'>Use the dashboard to review live health, incidents, agent decisions, and the current response queue.</p></div>", unsafe_allow_html=True)
with right:
    st.markdown(f"<div class='panel'><div class='section-label'>PLATFORM STATUS</div>{status_chip('Running')}<p class='muted' style='margin-top:.8rem'>Demo workspace • Simulated telemetry</p></div>", unsafe_allow_html=True)

st.write("")
cols = st.columns(4)
for col, args in zip(cols, [("Assets online", "42 / 45", "+2 since shift", "green"), ("Open incidents", "03", "1 critical", "red"), ("Agent confidence", "94.6%", "+1.8% today", "cyan"), ("Safety index", "91.2", "Within target", "green")]):
    with col:
        metric_card(*args)

st.write("")
st.markdown("<div class='panel'><div class='section-label'>QUICK START</div><p class='muted'>Navigate with the sidebar to inspect assets, simulate an incident, search the SOP knowledge base, or review AI agent activity.</p></div>", unsafe_allow_html=True)
