import streamlit as st


def render_investigation_progress():
    """Render the investigation progress with real-time status."""
    st.markdown("### 🤖 AI Investigation")
    
    # ✅ Check session state for progress
    if "investigation_stages" not in st.session_state:
        st.session_state.investigation_stages = [
            ("🛡️ Safety Analysis", "Pending"),
            ("🔍 Diagnostic Analysis", "Pending"),
            ("📚 Knowledge Retrieval", "Pending"),
            ("🔧 Maintenance Review", "Pending"),
            ("📋 Planning", "Pending"),
        ]
    
    # ✅ Update stages based on session state
    if st.session_state.get("investigation_complete", False):
        stages = [
            ("🛡️ Safety Analysis", "Completed"),
            ("🔍 Diagnostic Analysis", "Completed"),
            ("📚 Knowledge Retrieval", "Completed"),
            ("🔧 Maintenance Review", "Completed"),
            ("📋 Planning", "Completed"),
        ]
    else:
        stages = st.session_state.investigation_stages

    for stage, status in stages:
        left, right = st.columns([5, 1])
        
        with left:
            st.write(stage)
        
        with right:
            if status == "Completed":
                st.success("✅ Done")
            elif status == "Running":
                st.warning("⏳ Running...")
            else:
                st.info("⏸️ Pending")