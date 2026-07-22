import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page

setup_page("Settings")
render_sidebar("Settings")
page_heading("WORKSPACE CONFIGURATION", "Settings", "Configure how Command Nexus presents information and routes operational notifications.")

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>DISPLAY & WORKSPACE</div>", unsafe_allow_html=True)
    st.selectbox("Default facility", ["RigOS Alpha Refinery", "North Terminal", "Training Sandbox"])
    st.selectbox("Default dashboard range", ["Last 24 hours", "Current shift", "Last 7 days"])
    st.toggle("Compact data tables", value=False)
    st.toggle("Show simulated-data badge", value=True)
with right:
    st.markdown("<div class='section-label'>NOTIFICATIONS</div>", unsafe_allow_html=True)
    st.toggle("Critical incident alerts", value=True)
    st.toggle("Daily operational digest", value=True)
    st.toggle("Agent workflow-completion alerts", value=False)
    st.selectbox("Escalation policy", ["Standard operational", "High sensitivity", "Training mode"])

st.write("")
left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>AI CONFIGURATION</div>", unsafe_allow_html=True)
    st.selectbox("Response profile", ["Balanced", "Safety-first", "Speed-first"])
    st.slider("Recommendation confidence threshold", 50, 100, 85, 5)
with right:
    st.markdown("<div class='section-label'>INTEGRATION STATUS</div>", unsafe_allow_html=True)
    st.dataframe([{"Integration": "Telemetry service", "State": "Demo mode"}, {"Integration": "MAO kernel", "State": "Not connected"}, {"Integration": "Knowledge retrieval", "State": "Not connected"}, {"Integration": "Notifications", "State": "Not connected"}], hide_index=True, use_container_width=True)

st.info("Changes are retained only for the current Streamlit session in this UI prototype.")
st.button("Save workspace preferences")
# TODO: Persist preferences and integration secrets through authenticated backend settings endpoints.
