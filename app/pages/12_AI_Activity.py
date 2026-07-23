import streamlit as st

from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip
from frontend_services.agent_activity_adapter import (
    get_agent_activity,
    get_agent_metrics
)


setup_page("AI Activity")
render_sidebar("AI Activity Timeline")
page_heading("AUTONOMY AUDIT", "AI Agent Activity Timeline", "A chronological, reviewable record of AI observation, reasoning, and workflow handoffs.")
for col,args in zip(
    st.columns(4),
    get_agent_metrics()
):
    with col:
        metric_card(*args)

st.write("")
filter_col, search_col = st.columns([1, 2])
with filter_col:
    st.selectbox("Agent", ["All agents", "Safety", "Diagnostic", "Knowledge", "Maintenance", "Planning"])
with search_col:
    st.text_input("Search activity", placeholder="Filter by asset, workflow, or action")

st.markdown("<div class='section-label'>LIVE EXECUTION FLOW</div>", unsafe_allow_html=True)
for event in get_agent_activity():
    state_tone = "Running" if event["state"] == "Running" else ("Pending" if event["state"] == "Queued" else "Info")
    st.markdown(f"<div class='timeline-row'><span class='muted'>{event['time']}</span><span class='timeline-dot {'pulse' if event['state'] == 'Running' else ''}'></span><div class='panel'><b>{event['agent']}</b> &nbsp; {status_chip(state_tone)}<br><span class='muted'>{event['action']} · Confidence {event['confidence']}</span></div></div>", unsafe_allow_html=True)
    st.progress(event["progress"], text=f"{event['progress']}% execution progress")

# TODO: Read immutable agent lifecycle events and audit metadata from the MAO backend/event store.
