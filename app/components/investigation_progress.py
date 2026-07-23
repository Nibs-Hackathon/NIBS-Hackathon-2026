import streamlit as st


def render_investigation_progress():
    st.markdown("### 🤖 AI Investigation")

    stages = [
        ("🛡 Safety Analysis", "Completed"),
        ("🔍 Diagnostic Analysis", "Completed"),
        ("📚 Knowledge Retrieval", "Completed"),
        ("🔧 Maintenance Review", "Completed"),
        ("📋 Planning", "Completed"),
    ]

    for stage, status in stages:
        left, right = st.columns([5, 1])

        with left:
            st.write(stage)

        with right:
            st.success(status)