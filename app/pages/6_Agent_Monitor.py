import streamlit as st
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip

setup_page("Agent Monitor")
render_sidebar("Agent Monitor")
page_heading("AI SUPERVISION", "Agent Monitor", "Observe autonomous specialists, workflow handoffs, and decision confidence.")

for col, args in zip(st.columns(4), [("Agents online", "5 / 5", "All systems available", "green"), ("Workflows active", "02", "1 awaiting input", "amber"), ("Avg. confidence", "94.6%", "+1.8% today", "cyan"), ("Decisions today", "128", "Within review SLA", "violet")]):
    with col: metric_card(*args)

st.write("")
agents = [{"Agent": "Safety", "Specialty": "Risk validation", "State": "Active", "Confidence": "96%", "Current task": "Check Compressor C-12"}, {"Agent": "Diagnostic", "Specialty": "Root-cause analysis", "State": "Active", "Confidence": "95%", "Current task": "Analyze vibration pattern"}, {"Agent": "Knowledge", "Specialty": "SOP retrieval", "State": "Ready", "Confidence": "93%", "Current task": "Awaiting request"}, {"Agent": "Maintenance", "Specialty": "Maintenance planning", "State": "Ready", "Confidence": "94%", "Current task": "Awaiting task"}, {"Agent": "Planning", "Specialty": "Recovery planning", "State": "Queued", "Confidence": "92%", "Current task": "Prepare recovery sequence"}]
st.markdown("<div class='section-label'>AGENT FLEET</div>", unsafe_allow_html=True)
st.dataframe(agents, hide_index=True, use_container_width=True)

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>WORKFLOW PROGRESS</div>", unsafe_allow_html=True)
    st.progress(72, text="Vibration response workflow • 72% complete")
    st.progress(38, text="Pressure variance workflow • 38% complete")
with right:
    st.markdown("<div class='section-label'>LATEST HANDOFF</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'>{status_chip('Info')}<p><b>Diagnostic → Planning</b></p><span class='muted'>Root-cause confidence reached threshold. Recovery plan generation has been queued.</span></div>", unsafe_allow_html=True)
    # TODO: Surface live MAOKernel registry, scheduler, and report state here.
