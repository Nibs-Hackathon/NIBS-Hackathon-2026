import streamlit as st

from components.phase_one_views import render_agent_execution_view
from frontend_services.agent_adapter import get_agent_monitor_metrics, get_agents
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Agent Monitor")
render_sidebar("Agent Monitor")
page_heading("AI SUPERVISION", "Agent Monitor", "Registered MAO specialists and their latest runtime decisions.")

agents = get_agents()
for col, args in zip(st.columns(4), get_agent_monitor_metrics(agents)):
    with col:
        metric_card(*args)

st.write("")
st.markdown("<div class='section-label'>AGENT FLEET</div>", unsafe_allow_html=True)
if agents:
    st.dataframe(
        agents,
        hide_index=True,
        height=300,
        column_config={
            "Decision": st.column_config.TextColumn("Latest decision", width="large"),
            "Confidence": st.column_config.TextColumn("Confidence"),
        },
    )
    render_agent_execution_view(agents)
else:
    st.warning("No agents are registered with the shared MAO runtime.")

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>WORKFLOW PROGRESS</div>", unsafe_allow_html=True)
    active = [agent for agent in agents if agent["State"] in {"Ready", "Attention"}]
    if active:
        st.progress(100, text=f"{len(active)} agent(s) ready for the next approved workflow")
    else:
        st.caption("Workflow progress is available after the scheduler records an active task.")
with right:
    st.markdown("<div class='section-label'>LATEST HANDOFF</div>", unsafe_allow_html=True)
    latest = next((agent for agent in agents if agent["State"] != "Ready"), None)
    if latest:
        st.markdown(
            f"<div class='panel'>{status_chip(latest['State'])}<p><b>{latest['Agent']} agent</b></p>"
            f"<span class='muted'>{latest['Decision']} · {latest['Last execution']}</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("No agent handoff has been recorded yet.")
