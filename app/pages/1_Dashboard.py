import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ui_helpers import page_heading, render_sidebar, setup_page, metric_card, status_chip
from frontend_services.backend_api_new import api
from services.notification_service import notification_service, NotificationSeverity
from services.revenue_impact_calculator import revenue_service
from services.maintenance_scheduler import maintenance_scheduler
from components.global_notifications import render_global_notifications

setup_page("Dashboard")
render_sidebar("Executive Dashboard")

# ✅ RENDER GLOBAL NOTIFICATIONS
render_global_notifications()

page_heading(
    "🏭 REFINERY DASHBOARD",
    "Real-Time Operations Center",
    "Live health, revenue, incidents, and maintenance across all assets.",
)

# ✅ Initialize session state for real-time data
if "chart_data" not in st.session_state:
    st.session_state.chart_data = pd.DataFrame({
        "timestamp": [datetime.now()],
        "pressure": [110],
        "temperature": [70],
        "flow": [60],
        "vibration": [5],
        "gas": [2],
    })

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
    st.session_state.refresh_count = 0

# ✅ AUTO-REFRESH every 3 seconds
now = time.time()
if now - st.session_state.last_refresh >= 3:
    st.session_state.last_refresh = now
    st.session_state.refresh_count += 1
    st.rerun()

# ✅ Get real-time data
assets = api.get_assets()
incidents = api.get_incidents()

# ✅ Build telemetry data for chart
telemetry_data = []
for asset in assets[:20]:
    readings = api.get_asset_telemetry(asset["id"], limit=30)
    for r in readings:
        if isinstance(r, dict):
            sensor_type = r.get("sensor_type", "Unknown")
            value = r.get("value", 0)
            timestamp = r.get("timestamp", datetime.now().isoformat())
        else:
            sensor_type = getattr(r, 'sensor_type', 'Unknown')
            if hasattr(sensor_type, 'value'):
                sensor_type = sensor_type.value
            value = getattr(r, 'value', 0)
            timestamp = getattr(r, 'timestamp', datetime.now().isoformat())
        
        telemetry_data.append({
            "timestamp": timestamp,
            "asset": asset.get("name", "Unknown"),
            "value": float(value),
            "sensor_type": str(sensor_type),
        })

# ✅ Create DataFrame for chart
if telemetry_data:
    df = pd.DataFrame(telemetry_data)
    if not df.empty and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        
        pivot_df = df.pivot_table(
            index="timestamp", 
            columns="sensor_type", 
            values="value",
            aggfunc="mean"
        ).fillna(0)
        
        pivot_df = pivot_df.tail(30)
        
        st.markdown("<div class='section-label'>📡 LIVE TELEMETRY STREAM</div>", unsafe_allow_html=True)
        
        if not pivot_df.empty:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)
            
            available_cols = pivot_df.columns.tolist()
            
            sensor_config = {
                "Pressure": {"name": "Pressure (PSI)", "color": "#55D6FF", "row": 1},
                "Temperature": {"name": "Temperature (°C)", "color": "#FF8844", "row": 1},
                "Flow": {"name": "Flow (L/min)", "color": "#4FE3B2", "row": 2},
                "Vibration": {"name": "Vibration (mm/s)", "color": "#FF718D", "row": 2},
                "Gas": {"name": "Gas (ppm)", "color": "#9B8CFF", "row": 2},
            }
            
            for sensor_type, config in sensor_config.items():
                if sensor_type in available_cols:
                    fig.add_trace(
                        go.Scatter(
                            x=pivot_df.index, 
                            y=pivot_df[sensor_type], 
                            name=config["name"],
                            line=dict(color=config["color"], width=2), 
                            mode="lines+markers",
                            marker=dict(size=4),
                        ),
                        row=config["row"], col=1
                    )
            
            if len(fig.data) > 0:
                fig.update_layout(
                    height=400,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e8f0ff"),
                    hovermode="x unified",
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)")
                fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)")
                
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"🔄 Auto-refreshes every 3 seconds | {len(pivot_df)} data points | {len(available_cols)} sensor types")
            else:
                st.info("Waiting for telemetry data...")
        else:
            st.info("Collecting telemetry data...")
    else:
        st.info("No telemetry data available yet...")
else:
    # ✅ Fallback: Demo data
    st.markdown("<div class='section-label'>📡 LIVE TELEMETRY STREAM</div>", unsafe_allow_html=True)
    
    if "demo_chart_data" not in st.session_state:
        st.session_state.demo_chart_data = pd.DataFrame({
            "timestamp": [datetime.now() - timedelta(seconds=i) for i in range(30, 0, -1)],
            "Pressure": [105 + np.random.randn() * 2 for _ in range(30)],
            "Temperature": [72 + np.random.randn() * 1.5 for _ in range(30)],
            "Flow": [55 + np.random.randn() * 3 for _ in range(30)],
            "Vibration": [3 + np.random.randn() * 0.3 for _ in range(30)],
        })
    
    demo_df = st.session_state.demo_chart_data.tail(30)
    
    if not demo_df.empty:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)
        
        fig.add_trace(
            go.Scatter(x=demo_df["timestamp"], y=demo_df["Pressure"], name="Pressure (PSI)",
                       line=dict(color="#55D6FF", width=2), mode="lines+markers"),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=demo_df["timestamp"], y=demo_df["Temperature"], name="Temperature (°C)",
                       line=dict(color="#FF8844", width=2), mode="lines+markers"),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=demo_df["timestamp"], y=demo_df["Flow"], name="Flow (L/min)",
                       line=dict(color="#4FE3B2", width=2), mode="lines+markers"),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=demo_df["timestamp"], y=demo_df["Vibration"], name="Vibration (mm/s)",
                       line=dict(color="#FF718D", width=2), mode="lines+markers"),
            row=2, col=1
        )
        
        fig.update_layout(
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e8f0ff"),
            hovermode="x unified",
            margin=dict(l=10, r=10, t=10, b=10)
        )
        fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)")
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)")
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"🔄 Demo mode - waiting for real telemetry data | {len(demo_df)} data points")
    else:
        st.info("Waiting for telemetry data...")

st.write("---")

# ✅ Calculate metrics
total_assets = len(assets)
if total_assets > 0:
    healths = [a.get("health", 0) for a in assets]
    overall_health = round(sum(healths) / total_assets, 1)
    online = sum(1 for a in assets if a.get("status") in ["Running", "Healthy"])
    warning = sum(1 for a in assets if a.get("status") == "Warning")
    critical = sum(1 for a in assets if a.get("status") == "Critical")
    predicted_failures = sum(1 for a in assets if a.get("health", 100) < 60)
else:
    overall_health = 0
    online = 0
    warning = 0
    critical = 0
    predicted_failures = 0

# ✅ Revenue calculation
revenue_data = revenue_service.calculate_company_revenue_impact(assets)

# ✅ Maintenance tasks
upcoming_tasks = maintenance_scheduler.get_upcoming_tasks(days=7)
critical_tasks = [t for t in upcoming_tasks if t.priority.value == "critical"]
next_maintenance = upcoming_tasks[0].scheduled_date.strftime('%b %d, %H:%M') if upcoming_tasks else "None scheduled"

# ✅ METRIC CARDS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #4fe3b2;">
        <div class="metric-label">🏭 Overall Health</div>
        <div class="metric-value" style="color: {'#4fe3b2' if overall_health > 80 else '#ffbf69' if overall_health > 50 else '#ff718d'}">
            {overall_health}%
        </div>
        <div class="metric-delta" style="color: #4fe3b2;">{online} Online / {total_assets} Total</div>
        <div style="display: flex; gap: 8px; margin-top: 4px;">
            <span style="color: #4fe3b2; font-size: 0.7rem;">✅ {online}</span>
            <span style="color: #ffbf69; font-size: 0.7rem;">⚠️ {warning}</span>
            <span style="color: #ff718d; font-size: 0.7rem;">🔴 {critical}</span>
        </div>
        <div style="margin-top: 6px; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px;">
            <div style="width: {overall_health}%; height: 100%; background: {'#4fe3b2' if overall_health > 80 else '#ffbf69' if overall_health > 50 else '#ff718d'}; border-radius: 2px; transition: width 1s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #ff8844;">
        <div class="metric-label">💰 Revenue</div>
        <div class="metric-value" style="color: #4fe3b2;">${revenue_data.get('current_revenue', 0):,.0f}</div>
        <div class="metric-delta" style="color: #ffbf69;">⚠️ Loss: ${revenue_data.get('total_impact', 0):,.0f}</div>
        <div style="color: #8fa1ba; font-size: 0.7rem;">Efficiency: {revenue_data.get('revenue_efficiency', 0)}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #ff718d;">
        <div class="metric-label">🚨 Incidents</div>
        <div class="metric-value" style="color: {'#ff718d' if len(incidents) > 0 else '#4fe3b2'}">
            {len(incidents)}
        </div>
        <div class="metric-delta" style="color: #ff718d;">🔮 {predicted_failures} predicted in 24h</div>
        <div style="color: #8fa1ba; font-size: 0.7rem;">Today: {len([i for i in incidents if i.get('timestamp', '')[:10] == datetime.now().strftime('%Y-%m-%d')])}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #55D6FF;">
        <div class="metric-label">🔧 Maintenance</div>
        <div class="metric-value" style="color: #55D6FF;">{len(upcoming_tasks)}</div>
        <div class="metric-delta" style="color: #ff718d;">⚡ {len(critical_tasks)} Critical</div>
        <div style="color: #8fa1ba; font-size: 0.7rem;">Next: {next_maintenance}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ✅ SECOND ROW: Health Distribution (PIE CHART) + Quick Actions
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<div class='section-label'>📊 ASSET HEALTH DISTRIBUTION</div>", unsafe_allow_html=True)
    
    if assets:
        health_ranges = ["0-20", "21-40", "41-60", "61-80", "81-100"]
        counts = []
        colors = ["#ff718d", "#ff718d", "#ffbf69", "#55D6FF", "#4fe3b2"]
        
        for h_range in health_ranges:
            low, high = map(int, h_range.split("-"))
            count = sum(1 for a in assets if low <= a.get("health", 100) <= high)
            counts.append(count)
        
        fig = go.Figure(data=[go.Pie(
            labels=health_ranges,
            values=counts,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textposition='inside',
            hoverinfo='label+value+percent',
            showlegend=False,
        )])
        
        fig.update_layout(
            height=280,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e8f0ff", size=12),
            margin=dict(l=20, r=20, t=20, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        healthy = sum(1 for a in assets if a.get("health", 0) >= 80)
        warning = sum(1 for a in assets if 50 <= a.get("health", 0) < 80)
        critical = sum(1 for a in assets if a.get("health", 0) < 50)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
            <div style="text-align:center; padding:8px; background:rgba(79,227,178,0.1); border-radius:8px; border-left:3px solid #4fe3b2;">
                <div style="font-size:0.7rem; color:#8fa1ba;">HEALTHY</div>
                <div style="font-size:1.2rem; font-weight:700; color:#4fe3b2;">{healthy}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div style="text-align:center; padding:8px; background:rgba(255,191,105,0.1); border-radius:8px; border-left:3px solid #ffbf69;">
                <div style="font-size:0.7rem; color:#8fa1ba;">WARNING</div>
                <div style="font-size:1.2rem; font-weight:700; color:#ffbf69;">{warning}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown(f"""
            <div style="text-align:center; padding:8px; background:rgba(255,113,141,0.1); border-radius:8px; border-left:3px solid #ff718d;">
                <div style="font-size:0.7rem; color:#8fa1ba;">CRITICAL</div>
                <div style="font-size:1.2rem; font-weight:700; color:#ff718d;">{critical}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No assets available.")

with col2:
    st.markdown("<div class='section-label'>⚡ Quick Actions</div>", unsafe_allow_html=True)
    
    # ✅ UNIQUE KEYS for each button to avoid duplicate ID error
    if st.button("🔍 View Agent Monitor", key="btn_agent_monitor", use_container_width=True):
        st.switch_page("app/pages/6_Agent_Monitor.py")
    
    if st.button("📋 View AI Activity", key="btn_ai_activity", use_container_width=True):
        st.switch_page("app/pages/12_AI_Activity.py")
    
    if st.button("🚨 Trigger Test Incident", key="btn_test_incident", use_container_width=True):
        from frontend_services.incident_adapter import trigger_incident
        trigger_incident("pressure spike")
        st.success("✅ Test incident triggered!")
        time.sleep(1)
        st.rerun()

st.write("---")

# ✅ THIRD ROW: Top 5 Healthiest + Bottom 5 Needing Attention
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section-label'>🏆 Top 5 Healthiest Assets</div>", unsafe_allow_html=True)
    sorted_assets = sorted(assets, key=lambda x: x.get("health", 0), reverse=True)[:5]
    for a in sorted_assets:
        health = a.get("health", 0)
        color = "#4fe3b2" if health > 80 else "#ffbf69" if health > 50 else "#ff718d"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span style="color: #e8f0ff;">{a.get('name', 'Unknown')}</span>
            <span style="color: {color}; font-weight: 600;">{health:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-label'>⚠️ Top 5 Assets Needing Attention</div>", unsafe_allow_html=True)
    sorted_assets = sorted(assets, key=lambda x: x.get("health", 0))[:5]
    for a in sorted_assets:
        health = a.get("health", 0)
        color = "#4fe3b2" if health > 80 else "#ffbf69" if health > 50 else "#ff718d"
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span style="color: #e8f0ff;">{a.get('name', 'Unknown')}</span>
            <span style="color: {color}; font-weight: 600;">{health:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

# ✅ Footer
st.write("---")
st.caption(f"🔄 Auto-refreshes every 3 seconds | Last updated: {datetime.now().strftime('%H:%M:%S')} | Refresh #{st.session_state.refresh_count}")  