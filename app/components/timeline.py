import streamlit as st
from datetime import datetime


def render_timeline():
    """Render the incident timeline with real events - limited to last 10."""
    st.markdown("### ⏱️ Incident Timeline")
    
    if "incident_events" in st.session_state and st.session_state.incident_events:
        events = st.session_state.incident_events
        # ✅ Only show last 10 events
        events = events[-10:]
    else:
        events = [
            ("⏱️ 00:00", "🚨 Incident detected"),
            ("⏱️ 00:05", "✅ Investigation complete"),
        ]

    for time, event in events:
        st.markdown(
            f"""
            <div class="timeline-row" style="display: flex; gap: 12px; align-items: center; margin: 6px 0; padding: 8px 12px; background: rgba(255,255,255,0.03); border-radius: 8px;">
                <div style="color:#55D6FF;font-size:0.85rem;font-weight:600;min-width:80px;">{time}</div>
                <div style="width:10px;height:10px;border-radius:50%;background:#55D6FF;box-shadow:0 0 10px #55D6FF;"></div>
                <div style="color:#e8f0ff;">{event}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )