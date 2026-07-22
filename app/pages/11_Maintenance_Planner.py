import streamlit as st

from ui_helpers import metric_card, mock_maintenance_tasks, page_heading, render_sidebar, setup_page, status_chip


setup_page("Maintenance Planner")
render_sidebar("Maintenance Planner")
page_heading("WORK ORCHESTRATION", "Maintenance Planner", "Turn asset risk and AI recommendations into an executable maintenance plan.")

for col, args in zip(st.columns(4), [("Planned work", "12", "Across 4 crews", "cyan"), ("High priority", "02", "Needs today", "red"), ("Schedule load", "76%", "Within capacity", "green"), ("Predicted avoided risk", "18%", "Next 30 days", "violet")]):
    with col:
        metric_card(*args)

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>RECOMMENDED WORK PLAN</div>", unsafe_allow_html=True)
    st.dataframe(mock_maintenance_tasks(), hide_index=True, use_container_width=True, height=250)
with right:
    st.markdown("<div class='section-label'>PLANNING CONTROLS</div>", unsafe_allow_html=True)
    st.selectbox("Planning window", ["Next 7 days", "Next 14 days", "Next 30 days"])
    st.selectbox("Crew availability", ["All crews", "Rotating Equipment", "Utilities Crew", "Instrumentation"])
    st.button("Generate AI work plan", use_container_width=True)
    st.button("Balance schedule", use_container_width=True)
    st.caption("These controls are UI-only in the current prototype.")

st.write("")
left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>MAINTENANCE TIMELINE</div>", unsafe_allow_html=True)
    timeline = [("Today · 14:00", "Heat Exchanger H-03", "Utilities Crew", "P1", "2.5 h"), ("Tomorrow · 09:00", "Compressor C-12", "Rotating Equipment", "P2", "4.0 h"), ("25 Jul · 11:00", "Valve V-09", "Instrumentation", "P3", "1.5 h")]
    for window, asset, engineer, priority, downtime in timeline:
        st.markdown(f"<div class='timeline-row'><span class='muted'>{window}</span><span class='timeline-dot'></span><div class='panel'><b>{asset}</b> &nbsp; {status_chip('Critical' if priority == 'P1' else 'Warning')}<br><span class='muted'>Assigned engineer: {engineer} · Estimated downtime: {downtime}</span></div></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>AI SCHEDULING RATIONALE</div><div class='panel'><b>Optimized sequence</b><p class='muted'>Prioritizes the thermal-risk work order ahead of compressor inspection, while grouping pipeline work with instrumentation availability.</p><b>Expected impact</b><p class='muted'>Reduces forecasted operational risk by 18% and avoids overlap with peak production windows.</p></div>", unsafe_allow_html=True)

# TODO: Persist maintenance tasks, crew capacity, work-order status, and planning decisions through backend APIs.
