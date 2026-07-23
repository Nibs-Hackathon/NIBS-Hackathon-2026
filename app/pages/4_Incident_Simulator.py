
import sys
from pathlib import Path

import streamlit as st



ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from components.phase_one_views import render_incident_response_flow, render_live_signal_banner
from frontend_services.incident_adapter import trigger_incident
from ui_helpers import (
    incident_simulator_demo_flow,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip,
)
from components.incident_card import render_incident_card
from components.agent_card import render_agent_card
from components.telemetry_card import render_telemetry
from components.timeline import render_timeline
from components.investigation_progress import render_investigation_progress


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
    simulator_result = trigger_incident(
        incident_type
    )
    render_incident_card(
        asset,
        incident_type,
        severity,
        "AI Investigation Complete" if simulator_result["reports"] else "Processing"
    )

    render_telemetry()
    render_timeline()
    render_investigation_progress()

    reports = simulator_result["reports"]

    if reports:
        for report in reports:
            render_agent_card(report)
    else:
        st.warning("No incident generated.")

    st.markdown("### ✅ System Recommendation")

    st.info(
        """
### Recommended Operator Actions

- Reduce pump speed by **20%**
- Verify discharge valve position
- Inspect the pressure relief valve
- Monitor pressure for **5 minutes**
- Do not restart until pressure remains below **135 PSI**
"""
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("✅ Approve Response Plan"):
            st.success("Response approved.")

    with c2:
        if st.button("🔄 Run Investigation Again"):
            st.info("Investigation restarted.")

    with c3:
        if st.button("📄 Generate Incident Report"):
            st.success("Report generation coming soon.")



st.write("")
st.markdown(
    "<div class='section-label'>RECENT SIMULATED SCENARIOS</div>",
    unsafe_allow_html=True,
)

st.dataframe(
    [
        {
            "Scenario": "SIM-772",
            "Type": "Gas leak",
            "Asset": "Tank T-04",
            "Result": "Resolved",
            "Duration": "3m 14s",
        },
        {
            "Scenario": "SIM-771",
            "Type": "High vibration",
            "Asset": "Compressor C-12",
            "Result": "Review required",
            "Duration": "2m 47s",
        },
    ],
    hide_index=True,
    use_container_width=True,
)

