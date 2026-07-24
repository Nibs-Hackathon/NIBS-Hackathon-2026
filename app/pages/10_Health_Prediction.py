import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from ui_helpers import gauge_card, metric_card, page_heading, render_sidebar, setup_page
from frontend_services.asset_adapter import get_assets
from frontend_services.health_prediction_adapter import get_health_prediction

setup_page("Health Prediction")
render_sidebar("Predictive Health")
page_heading("PREDICTIVE INTELLIGENCE", "Asset Health Prediction", "Forecast degradation risk early enough to plan safe, efficient intervention.")

asset_snapshot = get_assets()
assets = asset_snapshot.get("assets", [])

if not assets:
    st.warning("No assets available. Start the simulation to generate telemetry data.")
    st.stop()

asset_names = [a.get("name", "Unknown") for a in assets]

left, right = st.columns([1, 1.5])
with left:
    selected_name = st.selectbox("Forecast asset", asset_names)
    horizon = st.select_slider("Forecast horizon", options=["7 days", "14 days", "30 days"], value="14 days")
    selected_asset = next((a for a in assets if a.get("name") == selected_name), assets[0])
    horizon_days = int(horizon.split()[0])
    
    # ✅ Check if we have telemetry data
    try:
        profile = get_health_prediction(selected_asset.get("id"), horizon_days)
    except Exception as e:
        st.error(f"Could not generate prediction: {e}")
        profile = None
    
    if profile:
        st.markdown(
            """
            <div class='panel'>
            <div class='section-label'>MODEL STATUS</div>
            <b>Forecast engine: LIVE TELEMETRY MODE</b>
            <p class='muted'>Prediction generated from asset telemetry history and current health calculations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Generate some telemetry data by running the simulation or triggering incidents.")

with right:
    if profile:
        st.markdown(f"<div class='section-label'>PROJECTED HEALTH · {selected_name.upper()}</div>", unsafe_allow_html=True)
        predicted = profile.get("predicted", {})
        if predicted:
            st.line_chart(predicted, height=280)
        else:
            st.info("No prediction data available yet.")
    else:
        st.info("Run simulation to generate prediction data.")

# ... rest of the page with checks for profile data