import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from components.phase_one_views import render_agent_execution_view, render_live_signal_banner
from ui_helpers import (
    metric_card,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip
)
from frontend_services.agent_adapter import get_agent_metrics, get_agents
from components.global_notifications import render_global_notifications


# ✅ RENDER GLOBAL NOTIFICATIONS


setup_page("Agent Monitor")
render_global_notifications()
render_sidebar("Agent Monitor")
page_heading("AI SUPERVISION", "Agent Monitor", "Observe autonomous specialists, workflow handoffs, and decision confidence.")
render_live_signal_banner("LIVE MAO REGISTRY", "Agent registration and completed execution state are read from the shared backend kernel.", "Info")
st.write("")

for col, args in zip(st.columns(4), get_agent_metrics()):
    with col: metric_card(*args)

st.write("")
agents = get_agents()
st.markdown("<div class='section-label'>AGENT FLEET</div>", unsafe_allow_html=True)
st.dataframe(agents, hide_index=True, use_container_width=True)

render_agent_execution_view(agents)
# Replace the placeholder workflow progress with real data
left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>WORKFLOW PROGRESS</div>", unsafe_allow_html=True)
    
    # ✅ Get real workflow progress from reports
    from app.frontend_services.backend_api_new import api
    reports = api.get_reports()
    
    if reports:
        for report in reports[-3:]:  # Show last 3 reports
            progress = 100 if report.get("success") else 50
            status = "Complete" if report.get("success") else "In Progress"
            st.progress(progress / 100, text=f"{report.get('workflow', 'Unknown')} • {status}")
    else:
        st.info("No workflows have been executed yet. Trigger an incident to see progress.")

with right:
    st.markdown("<div class='section-label'>LATEST HANDOFF</div>", unsafe_allow_html=True)
    
    # ✅ Get real agent handoff data
    activity = api.get_agent_activity(limit=10)
    if len(activity) >= 2:
        last = activity[-1]
        prev = activity[-2] if len(activity) >= 2 else None
        if prev:
            st.markdown(
                f"<div class='panel'>{status_chip('Info')}<p><b>{prev.get('agent_name', 'Unknown')} → {last.get('agent_name', 'Unknown')}</b></p>"
                f"<span class='muted'>{last.get('summary', 'Handoff completed.')[:100]}</span></div>",
                unsafe_allow_html=True
            )
        else:
            st.info("Waiting for agent handoffs...")
    else:
        st.info("No agent activity recorded yet.")