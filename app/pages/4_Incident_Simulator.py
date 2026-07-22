import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Incidents",
    page_icon="🚨",
    layout="wide"
)


st.title("🚨 Incident Center")

st.write(
    "AI-powered incident detection, analysis and response tracking"
)


# Temporary mock data
# Later Ashutosh will replace this with API data

incidents = [
    {
        "Incident": "Pressure Spike",
        "Asset": "Pump A",
        "Severity": "HIGH",
        "Status": "Resolved",
        "Agent": "Incident Commander"
    },
    {
        "Incident": "High Temperature",
        "Asset": "Pump B",
        "Severity": "MEDIUM",
        "Status": "Monitoring",
        "Agent": "Safety Agent"
    },
    {
        "Incident": "Gas Leak Detection",
        "Asset": "Tank A",
        "Severity": "CRITICAL",
        "Status": "Active",
        "Agent": "Safety Agent"
    }
]


df = pd.DataFrame(incidents)


st.subheader("Active Incidents")

st.dataframe(
    df,
    use_container_width=True
)


st.divider()


st.subheader("Incident Details")


selected = st.selectbox(
    "Select Incident",
    df["Incident"]
)


incident = df[
    df["Incident"] == selected
].iloc[0]


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Asset",
        incident["Asset"]
    )


with col2:
    st.metric(
        "Severity",
        incident["Severity"]
    )


with col3:
    st.metric(
        "Status",
        incident["Status"]
    )


st.divider()


st.subheader("🤖 AI Analysis")


if incident["Incident"] == "Pressure Spike":

    st.warning(
        """
        Possible cavitation detected.

        Recommended Actions:

        1. Reduce pump RPM
        2. Inspect discharge valve
        3. Check bearings and seals
        4. Verify pressure sensor
        """
    )


elif incident["Incident"] == "High Temperature":

    st.warning(
        """
        Temperature exceeds safe operating range.

        Recommended Actions:

        1. Check cooling system
        2. Inspect equipment load
        3. Monitor temperature trend
        """
    )


else:

    st.error(
        """
        Gas leak emergency.

        Recommended Actions:

        1. Activate emergency response
        2. Close nearby valves
        3. Evacuate affected area
        """
    )


st.subheader("Agent Response")


agents = [
    "🦺 Safety Agent",
    "🔧 Maintenance Agent",
    "📚 Knowledge Agent",
    "👷 Incident Commander"
]


for agent in agents:

    st.success(
        f"{agent} completed analysis"
    )