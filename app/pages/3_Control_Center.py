import streamlit as st


st.title("🚨 Incident Center")


incidents = [
    {
        "type":"Pressure Spike",
        "asset":"Pump A",
        "severity":"HIGH",
        "status":"Resolved"
    },
    {
        "type":"Temperature Rise",
        "asset":"Pump B",
        "severity":"MEDIUM",
        "status":"Monitoring"
    }
]


for incident in incidents:

    with st.expander(
        incident["type"]
    ):

        st.write(
            "Asset:",
            incident["asset"]
        )

        st.write(
            "Severity:",
            incident["severity"]
        )

        st.write(
            "Status:",
            incident["status"]
        )

        st.info(
            "AI Recommendation: Inspect equipment and follow SOP."
        )