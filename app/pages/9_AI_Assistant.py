import streamlit as st

from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_copilot_context_panel
from ui_helpers import append_copilot_backend_exchange, copilot_messages, page_heading, render_sidebar, setup_page


setup_page("AI Assistant")
render_sidebar("AI Operations Assistant")
page_heading("COPILOT", "AI Operations Assistant", "Ask for a concise operational brief, asset context, or safety-focused recommendation.")
render_live_signal_banner("COMMAND NEXUS ONLINE", "Your industrial operations copilot is ready for operational questions and shift support.", "Info")
st.write("")
messages = copilot_messages()

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>CONVERSATION</div>", unsafe_allow_html=True)
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
with right:
    render_copilot_context_panel()

prompt = st.chat_input("Ask Command Nexus...")
if prompt:
    with st.spinner("Command Nexus is preparing your response..."):
        append_copilot_backend_exchange(prompt)
    st.rerun()

# TODO: Route chat through an approved MAO chat/workflow endpoint when exposed.
# Never send Gemini keys to Streamlit or create a second MAOKernel here.
