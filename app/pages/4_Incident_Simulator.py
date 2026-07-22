import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page, status_chip
from services.incident_service import IncidentService
from services.runtime import simulator
setup_page("Incident Simulator")
render_sidebar("Incident Simulator")
page_heading("SCENARIO LAB", "Incident Simulator", "Safely exercise AI detection, triage, and response workflows using synthetic events.")

left, right = st.columns([1, 1.35])
with left:
    st.markdown("<div class='section-label'>CONFIGURE SCENARIO</div>", unsafe_allow_html=True)
    asset = st.selectbox("Affected asset", ["Compressor C-12", "Pump A-01", "Valve V-09", "Heat Exchanger H-03"])
    incident_type = st.selectbox("Incident type", ["Pressure spike", "High temperature", "Gas leak", "High vibration", "Flow restriction"])
    severity = st.select_slider("Severity", options=["Low", "Medium", "High", "Critical"], value="High")
    automated = st.toggle("Enable AI workflow", value=True)
    launched = st.button("Launch simulated incident", use_container_width=True)
with right:
    st.markdown("<div class='section-label'>SIMULATED RESPONSE PATH</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'><b>1. Detect</b><br><span class='muted'>Synthetic {incident_type.lower()} signal received from {asset}.</span><hr><b>2. Triage</b><br><span class='muted'>Classify severity, assess safety envelope, and create an incident record.</span><hr><b>3. Orchestrate</b><br><span class='muted'>Route specialist agents through the matching response workflow.</span><hr><b>4. Recommend</b><br><span class='muted'>Compile evidence, SOP guidance, and recovery actions for review.</span></div>", unsafe_allow_html=True)

if launched:

    st.success(
        f"Simulation launched for {asset}"
    )
    service = IncidentService(simulator)


    simulator_result = service.trigger_incident(
        incident_type
    )


    st.markdown(
        status_chip("Processing"),
        unsafe_allow_html=True
    )


    st.subheader("🚨 AI Response")


    reports = simulator_result["reports"]


    if reports:

        for report in reports:

            st.success(
                report.final_summary
            )

            st.write(
                "Recommendations:"
            )

            for recommendation in report.recommendations:

                st.write(
                    "-",
                    recommendation
                )

    else:

        st.warning(
            "No incident generated."
        )

st.write("")
st.markdown("<div class='section-label'>RECENT SIMULATED SCENARIOS</div>", unsafe_allow_html=True)
st.dataframe([{"Scenario": "SIM-772", "Type": "Gas leak", "Asset": "Tank T-04", "Result": "Resolved", "Duration": "3m 14s"}, {"Scenario": "SIM-771", "Type": "High vibration", "Asset": "Compressor C-12", "Result": "Review required", "Duration": "2m 47s"}], hide_index=True, use_container_width=True)
