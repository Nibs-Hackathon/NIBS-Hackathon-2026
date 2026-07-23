import streamlit as st
from components.phase_one_views import render_agent_execution_view, render_live_signal_banner
from ui_helpers import (
    metric_card,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip
)

from frontend_services.agent_adapter import get_agents

setup_page("Agent Monitor")
render_sidebar("Agent Monitor")
page_heading("AI SUPERVISION", "Agent Monitor", "Observe autonomous specialists, workflow handoffs, and decision confidence.")
render_live_signal_banner("DEMO AGENT STATE", "The current view preserves the existing demonstration data. Live registry and workflow state are pending backend integration.", "Info")
st.write("")

for col, args in zip(st.columns(4), [("Agents online", "5 / 5", "All systems available", "green"), ("Workflows active", "02", "1 awaiting input", "amber"), ("Avg. confidence", "94.6%", "+1.8% today", "cyan"), ("Decisions today", "128", "Within review SLA", "violet")]):
    with col: metric_card(*args)

st.write("")
agents = get_agents()
st.markdown("<div class='section-label'>AGENT FLEET</div>", unsafe_allow_html=True)
st.dataframe(agents, hide_index=True, use_container_width=True)

render_agent_execution_view(agents)

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>WORKFLOW PROGRESS</div>", unsafe_allow_html=True)
    st.progress(72, text="Vibration response workflow • 72% complete")
    st.progress(38, text="Pressure variance workflow • 38% complete")
with right:
    st.markdown("<div class='section-label'>LATEST HANDOFF</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'>{status_chip('Info')}<p><b>Diagnostic → Planning</b></p><span class='muted'>Root-cause confidence reached threshold. Recovery plan generation has been queued.</span></div>", unsafe_allow_html=True)
    # TODO: Surface live MAOKernel registry, scheduler, task, and report state
    # through an approved read-only backend integration; do not instantiate a kernel here.
