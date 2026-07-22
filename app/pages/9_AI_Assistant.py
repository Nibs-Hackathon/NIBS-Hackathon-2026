import streamlit as st

from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_copilot_context_panel
from ui_helpers import append_copilot_backend_exchange, copilot_diagnostics, copilot_messages, page_heading, render_sidebar, setup_page


setup_page("AI Assistant")
render_sidebar("AI Operations Assistant")
page_heading("COPILOT", "AI Operations Assistant", "Ask for a concise operational brief, asset context, or SOP-guided recommendation.")
render_live_signal_banner("COPILOT DEMO MODE", "This conversation uses the existing deterministic frontend demo. It is not connected to Gemini or MAO agents.", "Info")
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
    with st.status("Temporary backend diagnostics", expanded=True) as status:
        succeeded = append_copilot_backend_exchange(prompt, diagnostic_callback=status.write)
        status.update(
            label="Knowledge Agent response received" if succeeded else "Knowledge Agent request failed",
            state="complete" if succeeded else "error",
        )
    st.rerun()

with st.expander("Temporary backend diagnostics", expanded=False):
    diagnostics = copilot_diagnostics()
    if diagnostics:
        st.code("\n".join(diagnostics), language="text")
    else:
        st.caption("Submit a question to record the frontend-to-agent execution trace.")

# TODO: Route chat through an approved MAO chat/workflow endpoint when exposed.
# Never send Gemini keys to Streamlit or create a second MAOKernel here.
