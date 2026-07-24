import streamlit as st

from frontend_services.control_adapter import get_control_state
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Control Center")
render_sidebar("Control Center")
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

with right:
    st.markdown("<div class='section-label'>SUPERVISORY ACTIONS</div>", unsafe_allow_html=True)
    st.info(
        "Command actions are unavailable until an authenticated MAO command endpoint is registered."
    )
    st.button("Acknowledge monitored alerts", disabled=True, width="stretch")
    st.button("Request AI situation brief", disabled=True, width="stretch")
    st.button("Open emergency response checklist", disabled=True, width="stretch")
