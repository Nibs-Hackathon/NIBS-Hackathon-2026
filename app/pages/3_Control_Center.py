import streamlit as st
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip

setup_page("Control Center")
render_sidebar("Control Center")
page_heading("MISSION CONTROL", "Control Center", "A protected command surface for supervising facility-level operating state.")

for col, args in zip(st.columns(4), [("Facility mode", "RUNNING", "Stable production", "green"), ("Throughput", "82.4%", "+3.2% shift target", "cyan"), ("Safety systems", "12 / 12", "All armed", "green"), ("Response queue", "02", "Awaiting review", "amber")]):
    with col: metric_card(*args)

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>FACILITY STATE</div><h3>RigOS Alpha Refinery</h3><p class='muted'>All primary systems are operating within their configured envelope. AI supervision is active across five critical workflows.</p>" + status_chip("Running") + "</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<div class='section-label'>PROCESS ZONES</div>", unsafe_allow_html=True)
    st.dataframe([{"Zone": "Process A", "State": "Nominal", "Load": "78%", "Assets": 11}, {"Zone": "Process B", "State": "Monitoring", "Load": "86%", "Assets": 9}, {"Zone": "Terminal", "State": "Nominal", "Load": "69%", "Assets": 14}, {"Zone": "Utilities", "State": "Attention", "Load": "73%", "Assets": 8}], hide_index=True, use_container_width=True)
with right:
    st.markdown("<div class='section-label'>SUPERVISORY ACTIONS</div>", unsafe_allow_html=True)
    st.info("Controls are presentation-only in this demo. No operational commands are sent.")
    st.button("Acknowledge monitored alerts", use_container_width=True)
    st.button("Request AI situation brief", use_container_width=True)
    st.button("Open emergency response checklist", use_container_width=True)
    # TODO: Connect these controls to authenticated backend command/workflow endpoints.
