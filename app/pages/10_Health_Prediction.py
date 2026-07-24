import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ui_helpers import gauge_card, metric_card, page_heading, render_sidebar, setup_page
from frontend_services.asset_adapter import get_assets
from frontend_services.health_prediction_adapter import get_health_prediction
from components.global_notifications import render_global_notifications

setup_page("Health Prediction")
render_sidebar("Predictive Health")
render_global_notifications()

page_heading(
    "🔮 PREDICTIVE INTELLIGENCE",
    "Asset Health Prediction",
    "Forecast degradation risk early enough to plan safe, efficient intervention.",
)

asset_snapshot = get_assets()
assets = asset_snapshot.get("assets", [])

if not assets:
    st.warning("No assets available. Start the simulation to generate telemetry data.")
    st.stop()

asset_names = [a.get("name", "Unknown") for a in assets]

left, right = st.columns([1, 1.5])
with left:
    selected_name = st.selectbox("🎯 Forecast asset", asset_names)
    horizon = st.select_slider(
        "📊 Forecast horizon", 
        options=["7 days", "14 days", "30 days", "60 days", "90 days"], 
        value="14 days"
    )
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
                <div class='section-label'>📊 MODEL STATUS</div>
                <b>🚀 Forecast engine: LIVE TELEMETRY MODE</b>
                <p class='muted'>Prediction generated from asset telemetry history and current health calculations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # ✅ Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Health", f"{profile.get('health', 0)}%")
        with col2:
            st.metric("Failure Probability", profile.get('failure_probability', '0%'))
        with col3:
            st.metric("RUL", profile.get('rul', 'N/A'))
    else:
        st.info("Generate some telemetry data by running the simulation or triggering incidents.")

with right:
    if profile and profile.get("predicted"):
        st.markdown(f"<div class='section-label'>📈 PROJECTED HEALTH · {selected_name.upper()}</div>", unsafe_allow_html=True)
        
        predicted = profile.get("predicted", {})
        if predicted:
            pred_health = predicted.get("Predicted health", [])
            threshold = predicted.get("Intervention threshold", [])
            
            if pred_health:
                # ✅ Create DataFrame for line chart
                chart_data = pd.DataFrame({
                    "Predicted Health": pred_health,
                })
                
                # ✅ Add threshold if available
                if threshold:
                    chart_data["Intervention Threshold"] = threshold[:len(pred_health)]
                
                # ✅ Display as line chart
                st.line_chart(chart_data, height=300)
                st.caption(f"Forecast: {len(pred_health)} days ahead")
            else:
                st.info("No prediction data available yet.")
st.write("")

# ✅ Historical data and telemetry
if profile:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='section-label'>📉 HISTORICAL HEALTH TREND</div>", unsafe_allow_html=True)
        historical = profile.get("historical", {})
        if historical.get("Historical health"):
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(len(historical["Historical health"]))),
                y=historical["Historical health"],
                mode="lines+markers",
                name="Historical Health",
                line=dict(color="#4FE3B2", width=2),
                marker=dict(size=6, color="#4FE3B2"),
                fill="tozeroy",
                fillcolor="rgba(79, 227, 178, 0.1)",
            ))
            fig.update_layout(
                height=200,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e8f0ff"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No historical data available.")
    
    with col2:
        st.markdown("<div class='section-label'>📡 SUPPORTING TELEMETRY</div>", unsafe_allow_html=True)
        telemetry = profile.get("telemetry", [])
        if telemetry:
            st.dataframe(telemetry[-5:], hide_index=True, use_container_width=True)
        else:
            st.info("No telemetry data available.")

# ✅ Additional metrics
if profile:
    st.write("")
    st.markdown("<div class='section-label'>📊 PREDICTION DETAILS</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Health Score", f"{profile.get('health', 0)}%")
    with col2:
        st.metric("Remaining Useful Life", profile.get('rul', 'N/A'))
    with col3:
        st.metric("Failure Probability", profile.get('failure_probability', '0%'))
    with col4:
        st.metric("Model Confidence", profile.get('confidence', '0%'))