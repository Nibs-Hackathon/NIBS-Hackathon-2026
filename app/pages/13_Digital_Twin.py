import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import plotly.graph_objects as go
import random

from frontend_services.digital_twin_adapter import get_twin_assets
from ui_helpers import page_heading, render_sidebar, setup_page, status_chip
from components.global_notifications import render_global_notifications

setup_page("Digital Twin")
render_sidebar("Digital Twin")
render_global_notifications()

page_heading(
    "🏗️ FACILITY TOPOLOGY",
    "Digital Twin View",
    "A live operational map of facility zones, asset condition, and observed process signals.",
)

assets = get_twin_assets()
if not assets:
    st.info("No assets are registered with the shared MAO runtime.")
    st.stop()

# ✅ Create zone colors
zone_colors = {
    "Process A": "#55D6FF",
    "Process B": "#4FE3B2",
    "Terminal": "#FFBF69",
    "Utilities": "#9B8CFF",
    "Pipeline": "#FF718D",
    "Unassigned": "#8FA1BA",
}

# ✅ Create facility map with Plotly
st.markdown("<div class='section-label'>🗺️ FACILITY MAP VIEW</div>", unsafe_allow_html=True)

# ✅ Generate positions for assets
positions = []
for i, asset in enumerate(assets):
    # ✅ Position based on zone
    zone = asset.get("Zone", "Unassigned")
    if zone == "Process A":
        x, y = 2 + random.uniform(-0.8, 0.8), 4 + random.uniform(-0.8, 0.8)
    elif zone == "Process B":
        x, y = 6 + random.uniform(-0.8, 0.8), 4 + random.uniform(-0.8, 0.8)
    elif zone == "Terminal":
        x, y = 4 + random.uniform(-0.8, 0.8), 1 + random.uniform(-0.8, 0.8)
    elif zone == "Utilities":
        x, y = 1 + random.uniform(-0.8, 0.8), 3 + random.uniform(-0.8, 0.8)
    elif zone == "Pipeline":
        x, y = 3 + random.uniform(-0.8, 0.8), 5 + random.uniform(-0.8, 0.8)
    else:
        x, y = 5 + random.uniform(-0.8, 0.8), 3 + random.uniform(-0.8, 0.8)
    
    positions.append({"x": x, "y": y})

# ✅ Create scatter map
fig = go.Figure()

# ✅ Add zone labels
zone_positions = {
    "Process A": (2, 4.8),
    "Process B": (6, 4.8),
    "Terminal": (4, 1.8),
    "Utilities": (1, 3.8),
    "Pipeline": (3, 5.8),
}

for zone, (x, y) in zone_positions.items():
    fig.add_annotation(
        x=x, y=y,
        text=f"<b>{zone}</b>",
        showarrow=False,
        font=dict(size=12, color=zone_colors.get(zone, "#8FA1BA")),
        bgcolor="rgba(13,23,40,0.7)",
        bordercolor=zone_colors.get(zone, "#8FA1BA"),
        borderwidth=1,
        borderpad=4,
        opacity=0.8,
    )

# ✅ Add assets as nodes
for asset, pos in zip(assets, positions):
    health = asset.get("Health", 0)
    status = asset.get("Status", "Unknown")
    
    # ✅ Color based on health
    if health >= 80:
        color = "#4FE3B2"
        symbol = "circle"
    elif health >= 50:
        color = "#FFBF69"
        symbol = "diamond"
    else:
        color = "#FF718D"
        symbol = "x"
    
    # ✅ Size based on importance
    size = 20 + (health / 10)
    
    fig.add_trace(go.Scatter(
        x=[pos["x"]],
        y=[pos["y"]],
        mode="markers+text",
        marker=dict(
            size=size,
            color=color,
            symbol=symbol,
            line=dict(color="white", width=1),
            opacity=0.9,
        ),
        text=[f"<b>{asset.get('Asset', '')}</b><br>Health: {health}%"],
        textposition="middle center",
        textfont=dict(color="white", size=9),
        hoverinfo="text",
        hovertext=f"""
        <b>{asset.get('Asset', '')}</b><br>
        Zone: {asset.get('Zone', '')}<br>
        Health: {health}%<br>
        Status: {status}<br>
        Temperature: {asset.get('Temperature', 'N/A')}<br>
        Pressure: {asset.get('Pressure', 'N/A')}<br>
        RPM: {asset.get('RPM', 'N/A')}
        """,
        name=asset.get('Asset', ''),
    ))

# ✅ Update layout
fig.update_layout(
    height=500,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e8f0ff"),
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(
        range=[0, 8],
        showgrid=False,
        showticklabels=False,
        zeroline=False,
    ),
    yaxis=dict(
        range=[0, 7],
        showgrid=False,
        showticklabels=False,
        zeroline=False,
    ),
    showlegend=False,
    hovermode="closest",
    annotations=[
        dict(
            x=4, y=6.5,
            text="🏭 RigOS Alpha Refinery - Facility Map",
            showarrow=False,
            font=dict(size=16, color="#55D6FF"),
        )
    ]
)

# ✅ Add zone background
fig.add_shape(type="rect", x0=0.5, y0=3.5, x1=3.5, y1=5.5, fillcolor="rgba(85,214,255,0.05)", line=dict(color="rgba(85,214,255,0.2)"), layer="below")
fig.add_shape(type="rect", x0=4.5, y0=3.5, x1=7.5, y1=5.5, fillcolor="rgba(79,227,178,0.05)", line=dict(color="rgba(79,227,178,0.2)"), layer="below")
fig.add_shape(type="rect", x0=2.5, y0=0.5, x1=5.5, y1=2.5, fillcolor="rgba(255,191,105,0.05)", line=dict(color="rgba(255,191,105,0.2)"), layer="below")
fig.add_shape(type="rect", x0=0.5, y0=2.5, x1=2.5, y1=4.5, fillcolor="rgba(155,140,255,0.05)", line=dict(color="rgba(155,140,255,0.2)"), layer="below")

st.plotly_chart(fig, use_container_width=True)

st.write("")
st.markdown("<div class='section-label'>📋 ASSET DETAILS</div>", unsafe_allow_html=True)

# ✅ Asset selection
selected_name = st.selectbox("🔍 Inspect digital-twin asset", [asset["Asset"] for asset in assets])
selected = next(asset for asset in assets if asset["Asset"] == selected_name)

# ✅ Display asset details
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🆔 Asset", selected["Asset"])
with col2:
    st.metric("🏷️ Category", selected["Category"])
with col3:
    st.metric("📍 Zone", selected["Zone"])
with col4:
    st.metric("📊 Health", f"{selected['Health']}%", delta="Good" if selected['Health'] > 80 else "Warning" if selected['Health'] > 50 else "Critical")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🌡️ Temperature", selected["Temperature"])
with col2:
    st.metric("📈 Pressure", selected["Pressure"])
with col3:
    st.metric("🔄 RPM", selected["RPM"])
with col4:
    st.metric("⚠️ Failure Prob.", selected["Failure"])

st.markdown(f"""
<div style="padding: 16px; background: rgba(13,23,40,0.6); border-radius: 12px; border: 1px solid rgba(85,214,255,0.1); margin-top: 12px;">
    <b>🔧 Maintenance Recommendation</b>
    <p style="color: #c0d0e8; margin-top: 4px;">{selected['Recommendation']}</p>
</div>
""", unsafe_allow_html=True)

# ✅ Asset tiles
st.write("")
st.markdown("<div class='section-label'>🏗️ ALL ASSETS OVERVIEW</div>", unsafe_allow_html=True)

# ✅ Display assets in grid
cols = st.columns(4)
for i, asset in enumerate(assets):
    with cols[i % 4]:
        health = asset.get("Health", 0)
        color = "#4FE3B2" if health >= 80 else "#FFBF69" if health >= 50 else "#FF718D"
        
        st.markdown(f"""
        <div style="padding: 12px; background: rgba(13,23,40,0.4); border-radius: 8px; border-left: 4px solid {color}; margin-bottom: 8px;">
            <div style="font-weight: 600; color: #e8f0ff; font-size: 0.9rem;">{asset['Asset']}</div>
            <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                <span style="color: #8fa1ba; font-size: 0.7rem;">{asset['Category']}</span>
                <span style="color: {color}; font-weight: 600; font-size: 0.9rem;">{health}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)