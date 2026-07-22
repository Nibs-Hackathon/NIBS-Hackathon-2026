import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from components.phase_one_views import render_incident_response_flow, render_live_signal_banner
from services.incident_service import IncidentService
from services.runtime import simulator
from ui_helpers import (
    incident_simulator_demo_flow,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip,
)


setup_page("Incident Simulator")
render_sidebar("Incident Simulator")
page_heading(
    "SCENARIO LAB",
    "Incident Simulator",
    "Safely exercise AI detection, triage, and response workflows using synthetic events.",
)
render_live_signal_banner(
    "SCENARIO DESIGN MODE",
    "This interface visualizes the existing simulator flow and runs approved synthetic scenarios.",
    "Info",
)
st.write("")

left, right = st.columns([1, 1.35])
with left:
    st.markdown("<div class='section-label'>CONFIGURE SCENARIO</div>", unsafe_allow_html=True)
    asset = st.selectbox("Affected asset", ["Compressor C-12", "Pump A-01", "Valve V-09", "Heat Exchanger H-03"])
    incident_type = st.selectbox("Incident type", ["Pressure spike", "High temperature", "Gas leak", "High vibration", "Flow restriction"])
    severity = st.select_slider("Severity", options=["Low", "Medium", "High", "Critical"], value="High")
    automated = st.toggle("Enable AI workflow", value=True)
    launched = st.button("Launch simulated incident", use_container_width=True)
with right:
    render_incident_response_flow(incident_simulator_demo_flow(incident_type, asset))

if launched:
    st.success(f"Simulation launched for {asset}")
    service = IncidentService(simulator)
    simulator_result = service.trigger_incident(incident_type)
    st.markdown(status_chip("Processing"), unsafe_allow_html=True)
    st.subheader("🚨 AI Response")

    reports = simulator_result["reports"]
    if reports:
        for report in reports:
            st.success(report.final_summary)
            st.write("Recommendations:")
            for recommendation in report.recommendations:
                st.write("-", recommendation)
    else:
        st.warning("No incident generated.")

st.write("")
st.markdown("<div class='section-label'>RECENT SIMULATED SCENARIOS</div>", unsafe_allow_html=True)
st.dataframe(
    [
        {"Scenario": "SIM-772", "Type": "Gas leak", "Asset": "Tank T-04", "Result": "Resolved", "Duration": "3m 14s"},
        {"Scenario": "SIM-771", "Type": "High vibration", "Asset": "Compressor C-12", "Result": "Review required", "Duration": "2m 47s"},
    ],
    hide_index=True,
    use_container_width=True,
)
