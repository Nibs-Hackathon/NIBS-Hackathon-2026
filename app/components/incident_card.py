import streamlit as st
from services.ai_config import AIConfigGenerator


def render_incident_card(asset, incident_type, severity, status="Processing"):
    """Render an incident card with dynamic severity colors."""
    
    # ✅ Get severity mapping from config
    try:
        config = AIConfigGenerator()
        severity_map = config.get_config().get("severity_mapping", {
            "Critical": 1, "High": 2, "Medium": 3, "Low": 4
        })
        severity_colors = {
            "Critical": "#ff5555",
            "High": "#ff8844",
            "Medium": "#ffbf69",
            "Low": "#4fe3b2",
        }
    except:
        severity_colors = {
            "Critical": "#ff5555",
            "High": "#ff8844",
            "Medium": "#ffbf69",
            "Low": "#4fe3b2",
        }
    
    color = severity_colors.get(severity, "#ffbf69")
    
    st.markdown(
        f"""
        <div class="incident-card" style="background:rgba(255,255,255,0.05);border:1px solid {color}44;border-radius:12px;padding:16px;margin:12px 0;">
            <h2 style="color:{color};margin:0 0 8px 0;">🚨 {incident_type}</h2>
            <p style="margin:4px 0;"><b>Asset:</b> {asset}</p>
            <p style="margin:4px 0;">
                <b>Severity:</b>
                <span style="color:{color};font-weight:bold;">
                    {severity}
                </span>
            </p>
            <p style="margin:4px 0;"><b>Status:</b> {status}</p>
        </div>
        """,
        unsafe_allow_html=True
    )