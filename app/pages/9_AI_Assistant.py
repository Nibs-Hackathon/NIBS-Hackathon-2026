import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_copilot_context_panel
from ui_helpers import append_copilot_backend_exchange, copilot_messages, page_heading, render_sidebar, setup_page
from components.global_notifications import render_global_notifications


setup_page("AI Assistant")
render_global_notifications()
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