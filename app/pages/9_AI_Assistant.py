import streamlit as st

from ui_helpers import page_heading, render_sidebar, setup_page


setup_page("AI Assistant")
render_sidebar("AI Operations Assistant")
page_heading("COPILOT", "AI Operations Assistant", "Ask for a concise operational brief, asset context, or SOP-guided recommendation.")

if "ops_messages" not in st.session_state:
    st.session_state.ops_messages = [
        {
            "role": "assistant",
            "content": "I’m the Command Nexus copilot. I can summarize simulated operations, explain active incidents, and draft maintenance actions.",
        }
    ]

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>CONVERSATION</div>", unsafe_allow_html=True)
    for message in st.session_state.ops_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
with right:
    st.markdown("<div class='section-label'>CONTEXT IN USE</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'><b>Demo facility</b><p class='muted'>RigOS Alpha Refinery</p><b>Priority signal</b><p class='muted'>Compressor C-12 vibration watch</p><b>Knowledge mode</b><p class='muted'>Simulated SOP retrieval</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>SUGGESTED PROMPTS</div>", unsafe_allow_html=True)
    st.caption("• Give me a shift brief\n\n• Why is Compressor C-12 under watch?\n\n• Draft a safe maintenance plan")

prompt = st.chat_input("Ask Command Nexus...")
if prompt:
    st.session_state.ops_messages.append({"role": "user", "content": prompt})
    response = "Demo response: I would combine current telemetry, open incidents, and retrieved SOP guidance before recommending an action. Backend-connected answers will appear here."
    st.session_state.ops_messages.append({"role": "assistant", "content": response})
    st.rerun()

# TODO: Send chat messages and selected facility context to a backend AI/RAG endpoint.
