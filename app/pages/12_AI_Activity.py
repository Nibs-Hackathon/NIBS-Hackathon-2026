import streamlit as st

from frontend_services.agent_activity_adapter import get_agent_activity, get_agent_metrics
from frontend_services.agent_adapter import get_agents
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("AI Activity")
render_sidebar("AI Activity Timeline")
page_heading("AUTONOMY AUDIT", "AI Agent Activity Timeline", "Chronological evidence of live MAO execution and persisted audit events.")

for col, args in zip(st.columns(4), get_agent_metrics()):
    with col:
        metric_card(*args)

events, activity_warning = get_agent_activity()
if activity_warning:
    st.caption(activity_warning)

agent_names = [agent["Agent"] for agent in get_agents()]
filter_col, search_col = st.columns([1, 2])
with filter_col:
    agent_filter = st.selectbox("Agent", ["All agents"] + agent_names)
with search_col:
    search_term = st.text_input("Search activity", placeholder="Filter by agent or decision")

st.markdown("<div class='section-label'>LIVE EXECUTION FLOW</div>", unsafe_allow_html=True)
visible_events = [
    event
    for event in events
    if (agent_filter == "All agents" or event["agent"].replace("_", " ").title() == agent_filter)
    and (not search_term.strip() or search_term.lower() in f"{event['agent']} {event['action']}".lower())
]

if not visible_events:
    st.info("No matching MAO activity has been recorded yet.")

for event in visible_events:
    state = event["state"]
    state_tone = "Running" if state.lower() == "running" else ("Pending" if state.lower() in {"queued", "pending"} else ("Completed" if state.lower() == "completed" else "Attention"))
    st.markdown(
        f"<div class='timeline-row'><span class='muted'>{event['time']}</span>"
        f"<span class='timeline-dot {'pulse' if state_tone == 'Running' else ''}'></span>"
        f"<div class='panel'><b>{event['agent'].replace('_', ' ').title()}</b> &nbsp; {status_chip(state_tone)}"
        f"<br><span class='muted'>{event['action']} · Confidence {event['confidence']}</span></div></div>",
        unsafe_allow_html=True,
    )
    st.progress(event["progress"], text=f"{event['progress']}% execution progress")
