import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page
from components.global_notifications import render_global_notifications

setup_page("Settings")
render_global_notifications()
render_sidebar("Settings")
page_heading("WORKSPACE CONFIGURATION", "Settings", "Configure how Command Nexus presents information and routes operational notifications.")

# Initialize session state for settings
if "settings" not in st.session_state:
    st.session_state.settings = {
        "facility": "RigOS Alpha Refinery",
        "dashboard_range": "Last 24 hours",
        "compact_tables": False,
        "show_sim_badge": True,
        "critical_alerts": True,
        "daily_digest": True,
        "agent_completion_alerts": False,
        "escalation_policy": "Standard operational",
        "response_profile": "Balanced",
        "confidence_threshold": 85,
    }

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>DISPLAY & WORKSPACE</div>", unsafe_allow_html=True)
    facility = st.selectbox(
        "Default facility",
        ["RigOS Alpha Refinery", "North Terminal", "Training Sandbox"],
        index=["RigOS Alpha Refinery", "North Terminal", "Training Sandbox"].index(st.session_state.settings["facility"])
    )
    dashboard_range = st.selectbox(
        "Default dashboard range",
        ["Last 24 hours", "Current shift", "Last 7 days"],
        index=["Last 24 hours", "Current shift", "Last 7 days"].index(st.session_state.settings["dashboard_range"])
    )
    compact_tables = st.toggle("Compact data tables", value=st.session_state.settings["compact_tables"])
    show_sim_badge = st.toggle("Show simulated-data badge", value=st.session_state.settings["show_sim_badge"])

with right:
    st.markdown("<div class='section-label'>NOTIFICATIONS</div>", unsafe_allow_html=True)
    critical_alerts = st.toggle("Critical incident alerts", value=st.session_state.settings["critical_alerts"])
    daily_digest = st.toggle("Daily operational digest", value=st.session_state.settings["daily_digest"])
    agent_completion_alerts = st.toggle("Agent workflow-completion alerts", value=st.session_state.settings["agent_completion_alerts"])
    escalation_policy = st.selectbox(
        "Escalation policy",
        ["Standard operational", "High sensitivity", "Training mode"],
        index=["Standard operational", "High sensitivity", "Training mode"].index(st.session_state.settings["escalation_policy"])
    )

st.write("")
left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>AI CONFIGURATION</div>", unsafe_allow_html=True)
    response_profile = st.selectbox(
        "Response profile",
        ["Balanced", "Safety-first", "Speed-first"],
        index=["Balanced", "Safety-first", "Speed-first"].index(st.session_state.settings["response_profile"])
    )
    confidence_threshold = st.slider(
        "Recommendation confidence threshold",
        50, 100, st.session_state.settings["confidence_threshold"], 5
    )

with right:
    st.markdown("<div class='section-label'>INTEGRATION STATUS</div>", unsafe_allow_html=True)
    st.dataframe([
        {"Integration": "Telemetry service", "State": "Active ✅" if st.session_state.settings.get("telemetry_connected", False) else "Demo mode"},
        {"Integration": "MAO kernel", "State": "Connected ✅" if st.session_state.settings.get("mao_connected", False) else "Not connected"},
        {"Integration": "Knowledge retrieval", "State": "Active ✅" if st.session_state.settings.get("knowledge_connected", False) else "Not connected"},
        {"Integration": "Notifications", "State": "Ready" if st.session_state.settings.get("notifications_enabled", False) else "Not connected"},
    ], hide_index=True, use_container_width=True)

# Save button
if st.button("💾 Save workspace preferences", use_container_width=True):
    st.session_state.settings.update({
        "facility": facility,
        "dashboard_range": dashboard_range,
        "compact_tables": compact_tables,
        "show_sim_badge": show_sim_badge,
        "critical_alerts": critical_alerts,
        "daily_digest": daily_digest,
        "agent_completion_alerts": agent_completion_alerts,
        "escalation_policy": escalation_policy,
        "response_profile": response_profile,
        "confidence_threshold": confidence_threshold,
    })
    st.success("✅ Settings saved successfully!")
    st.balloons()

st.info("Changes are retained for the current Streamlit session. Refresh the page to reset.")