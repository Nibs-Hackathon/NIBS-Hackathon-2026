import streamlit as st

from frontend_services.agent_activity_adapter import get_agent_activity, get_agent_metrics
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("AI Activity")
render_sidebar("AI Activity Timeline")
page_heading(
    "AUTONOMY AUDIT",
    "AI Agent Activity Timeline",
    "A chronological, reviewable record of AI observation, reasoning, and workflow handoffs.",
)

for col, args in zip(st.columns(4), get_agent_metrics()):
    with col:
        metric_card(*args)

st.write("")
filter_col, search_col = st.columns([1, 2])
with filter_col:
    agent_filter = st.selectbox(
        "Agent",
        ["All agents", "Safety", "Diagnostic", "Knowledge", "Maintenance", "Planning"],
    )
with search_col:
    search_term = st.text_input(
        "Search activity", placeholder="Filter by asset, workflow, or action"
    )

st.markdown("<div class='section-label'>LIVE EXECUTION FLOW</div>", unsafe_allow_html=True)
events, activity_warning = get_agent_activity()
if activity_warning:
    st.caption(activity_warning)

visible_events = [
    event
    for event in events
    if (agent_filter == "All agents" or event["agent"].lower() == agent_filter.lower())
    and (
        not search_term.strip()
        or search_term.lower() in f"{event['agent']} {event['action']}".lower()
    )
]

if not visible_events:
    st.info("No matching MAO activity has been recorded yet.")

for event in visible_events:
    state_tone = (
        "Running"
        if event["state"] == "Running"
        else ("Pending" if event["state"] == "Queued" else "Info")
    )
    st.markdown(
        f"<div class='timeline-row'><span class='muted'>{event['time']}</span>"
        f"<span class='timeline-dot {'pulse' if event['state'] == 'Running' else ''}'></span>"
        f"<div class='panel'><b>{event['agent']}</b> &nbsp; {status_chip(state_tone)}"
        f"<br><span class='muted'>{event['action']} Â· Confidence {event['confidence']}"
        f"</span></div></div>",
        unsafe_allow_html=True,
    )
    st.progress(event["progress"], text=f"{event['progress']}% execution progress")
