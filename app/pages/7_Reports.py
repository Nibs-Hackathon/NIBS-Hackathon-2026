import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Incident Reports")

st.write(
    "Generated reports from MAO agents and incident analysis"
)


# Temporary mock data
# Later Ashutosh connects this to backend reports API

reports = [
    {
        "Incident": "Pressure Spike",
        "Asset": "Pump A",
        "Severity": "HIGH",
        "Confidence": "95%",
        "Status": "Completed"
    },
    {
        "Incident": "Gas Leak",
        "Asset": "Tank A",
        "Severity": "CRITICAL",
        "Confidence": "96%",
        "Status": "Completed"
    }
]


df = pd.DataFrame(reports)


st.subheader("Report History")

st.dataframe(
    df,
    use_container_width=True
)


st.divider()


st.subheader("Detailed AI Report")


selected = st.selectbox(
    "Select Report",
    df["Incident"]
)


if selected == "Pressure Spike":

    st.header("🚨 Pressure Spike Report")


    col1, col2, col3 = st.columns(3)


    with col1:
        st.metric(
            "Asset",
            "Pump A"
        )

    with col2:
        st.metric(
            "Severity",
            "HIGH"
        )

    with col3:
        st.metric(
            "Confidence",
            "95%"
        )


    st.divider()


    st.subheader("Root Cause Analysis")

    st.write(
        """
        Possible cavitation detected.

        Pressure exceeded safe operating limits.
        """
    )


    st.subheader("Agent Findings")


    findings = [
        "🦺 Safety Agent: Operating limits verified",
        "🔧 Maintenance Agent: Inspect pump bearings",
        "📚 Knowledge Agent: Retrieved pressure SOP",
        "👷 Incident Commander: Response plan created"
    ]


    for item in findings:
        st.success(item)



    st.subheader("Recommendations")


    recommendations = [
        "Reduce pump RPM by 20%",
        "Inspect discharge valve",
        "Check seals and bearings",
        "Monitor pressure recovery"
    ]


    for rec in recommendations:
        st.write(
            f"✅ {rec}"
        )


elif selected == "Gas Leak":

    st.header("🔥 Gas Leak Emergency Report")


    st.error(
        """
        Gas concentration exceeded safety threshold.
        """
    )


    st.subheader("Actions Taken")

    actions = [
        "Emergency response activated",
        "Nearby valves closed",
        "Personnel evacuation initiated",
        "Ventilation activated"
    ]


    for action in actions:
        st.write(
            f"✅ {action}"
        )