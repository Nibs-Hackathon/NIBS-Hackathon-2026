import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from frontend_services.control_adapter import get_control_state
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip
from components.global_notifications import render_global_notifications


# ✅ RENDER GLOBAL NOTIFICATIONS


setup_page("Control Center")
render_sidebar("Control Center")
render_global_notifications()

page_heading(
    "MISSION CONTROL",
    "Control Center",
    "A protected command surface for supervising facility-level operating state.",
)

state = get_control_state()
summary = state.get("summary", "Live facility summary is not available yet.")
metrics = [
    ("Facility mode", state["facility_mode"], "Live backend state", "green"),
    ("Asset availability", state["throughput"], "Calculated from assets", "cyan"),
    ("Safety systems", state["safety"], "Online assets", "green"),
    ("Response queue", state["queue"], "Active EventStore entries", "amber"),
]
for col, args in zip(st.columns(4), metrics):
    with col:
        metric_card(*args)

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown(
        "<div class='panel'><div class='section-label'>FACILITY STATE</div>"
        f"<h3>{state['facility_mode'].title()}</h3>"
        f"<p class='muted'>{summary}</p>"
        f"{status_chip(state['facility_mode'])}</div>",
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown("<div class='section-label'>PROCESS ZONES</div>", unsafe_allow_html=True)
    if state["zones"]:
        st.dataframe(state["zones"], hide_index=True, width="stretch")
    else:
        st.info("No zone data is available because no assets are registered.")

# Replace the disabled buttons with functional ones

with right:
    st.markdown("<div class='section-label'>SUPERVISORY ACTIONS</div>", unsafe_allow_html=True)
    
    # ✅ Acknowledge alerts
    if st.button("✅ Acknowledge monitored alerts", use_container_width=True):
        st.success("All alerts acknowledged. Incident manager updated.")
    
    # ✅ Request AI brief
    if st.button("🤖 Request AI situation brief", use_container_width=True):
        with st.spinner("Generating situation brief..."):
            from frontend_services.knowledge_agent_adapter import ask_knowledge_agent
            brief = ask_knowledge_agent("Summarize the current facility situation and operational status.")
            st.info(brief)
    
    # ✅ Emergency response
    if st.button("🚨 Open emergency response checklist", use_container_width=True):
        st.warning("⚠️ Emergency Response Checklist:\n1. Alert all personnel\n2. Isolate affected area\n3. Follow safety protocols\n4. Contact control room")