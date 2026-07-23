import streamlit as st


def render_incident_card(
    asset,
    incident_type,
    severity,
    status="Processing"
):

    st.markdown(
        f"""
        <div class="incident-card">

        <h2>🚨 {incident_type}</h2>

        <p>
        <b>Asset:</b> {asset}
        </p>

        <p>
        <b>Severity:</b>
        <span style="color:#ff5555">
        {severity}
        </span>
        </p>

        <p>
        <b>Status:</b> {status}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )