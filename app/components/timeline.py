import streamlit as st


def render_timeline():
    st.markdown("### ⏱ Incident Timeline")

    events = [
        ("10:42:01", "🚨 Pressure spike detected"),
        ("10:42:03", "🛡 Safety Agent executed"),
        ("10:42:05", "🔍 Diagnostic completed"),
        ("10:42:08", "📚 Knowledge retrieved"),
        ("10:42:10", "🔧 Maintenance recommended"),
        ("10:42:12", "📋 Planning completed"),
    ]

    for time, event in events:
        st.markdown(
            f"""
            <div class="timeline-row">
                <div style="color:#8fa1ba;font-size:0.9rem;">{time}</div>
                <div class="timeline-dot"></div>
                <div>{event}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )