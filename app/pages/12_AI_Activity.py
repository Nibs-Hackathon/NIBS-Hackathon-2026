import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

from frontend_services.agent_activity_adapter import get_agent_activity, get_agent_metrics
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip
from components.global_notifications import render_global_notifications

setup_page("AI Activity")
render_sidebar("AI Activity Timeline")
render_global_notifications()

page_heading(
    "🤖 AUTONOMY AUDIT",
    "AI Agent Activity Timeline",
    "A chronological, reviewable record of AI observation, reasoning, and workflow handoffs.",
)

# ✅ Display metrics
for col, args in zip(st.columns(4), get_agent_metrics()):
    with col:
        metric_card(*args)

st.write("")

# ✅ Activity heatmap
st.markdown("<div class='section-label'>🔥 AGENT ACTIVITY HEATMAP</div>", unsafe_allow_html=True)

events, activity_warning = get_agent_activity()

if events:
    # ✅ Prepare data for heatmap
    df = pd.DataFrame(events)
    
    if "agent" in df.columns and "timestamp" in df.columns:
        # ✅ Extract hour from timestamp
        df["hour"] = df["timestamp"].apply(
            lambda x: x.hour if isinstance(x, datetime) else 
            (datetime.fromisoformat(x).hour if isinstance(x, str) else 0)
        )
        df["day"] = df["timestamp"].apply(
            lambda x: x.strftime("%Y-%m-%d") if isinstance(x, datetime) else
            (datetime.fromisoformat(x).strftime("%Y-%m-%d") if isinstance(x, str) else "Unknown")
        )
        
        # ✅ Aggregate by agent and hour
        if "agent" in df.columns and "hour" in df.columns:
            heatmap_data = df.groupby(["agent", "hour"]).size().reset_index(name="count")
            
            # ✅ Pivot for heatmap
            pivot = heatmap_data.pivot(index="agent", columns="hour", values="count").fillna(0)
            
            # ✅ Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                colorscale="Viridis",
                hovertemplate="Agent: %{y}<br>Hour: %{x}:00<br>Activities: %{z}<extra></extra>",
            ))
            
            fig.update_layout(
                height=300,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e8f0ff"),
                margin=dict(l=100, r=20, t=20, b=40),
                xaxis=dict(
                    title="Hour of Day",
                    tickmode="array",
                    tickvals=list(range(0, 24, 2)),
                    ticktext=[f"{h}:00" for h in range(0, 24, 2)],
                    gridcolor="rgba(255,255,255,0.05)",
                ),
                yaxis=dict(
                    title="Agent",
                    gridcolor="rgba(255,255,255,0.05)",
                ),
                coloraxis_colorbar=dict(
                    title="Activity Count",
                    tickfont=dict(color="#e8f0ff"),
                ),
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No agent data available for heatmap.")
    else:
        st.info("No timestamp data available for heatmap.")
else:
    st.info("No activity data available yet.")

st.write("")

# ✅ Filter and search
filter_col, search_col = st.columns([1, 2])
with filter_col:
    agent_filter = st.selectbox(
        "🎯 Filter by Agent",
        ["All agents", "Safety", "Diagnostic", "Knowledge", "Maintenance", "Planning", "Sensor", "Prediction", "Notification", "Report"],
    )
with search_col:
    search_term = st.text_input(
        "🔍 Search activity", 
        placeholder="Filter by asset, workflow, or action"
    )

st.markdown("<div class='section-label'>📋 LIVE EXECUTION FLOW</div>", unsafe_allow_html=True)

if activity_warning:
    st.caption(activity_warning)

# ✅ Filter events
visible_events = [
    event
    for event in events
    if (agent_filter == "All agents" or event["agent"].lower() == agent_filter.lower())
    and (
        not search_term.strip()
        or search_term.lower() in f"{event['agent']} {event['action']}".lower()
    )
]

if not visible_events:
    st.info("No matching MAO activity has been recorded yet.")
else:
    # ✅ Display events
    for i, event in enumerate(visible_events[:50]):
        state_tone = (
            "Running"
            if event["state"] == "Running"
            else ("Pending" if event["state"] == "Queued" else "Info")
        )
        
        # ✅ Color coding based on state
        dot_color = "#55D6FF" if event["state"] == "Completed" else "#FFBF69" if event["state"] == "Running" else "#8FA1BA"
        
        st.markdown(
            f"""
            <div class='timeline-row'>
                <span class='muted'>{event['time']}</span>
                <span class='timeline-dot' style="background: {dot_color}; box-shadow: 0 0 14px {dot_color};"></span>
                <div class='panel'>
                    <b>{event['agent']}</b>
                    <span style="margin-left: 8px;">{status_chip(state_tone)}</span>
                    <br>
                    <span class='muted'>{event['action']} · Confidence {event['confidence']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(event["progress"] / 100, text=f"{event['progress']}% execution progress")

# ✅ Summary stats
if visible_events:
    st.write("")
    st.markdown("<div class='section-label'>📊 ACTIVITY SUMMARY</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Events", len(visible_events))
    with col2:
        completed = sum(1 for e in visible_events if e["state"] == "Completed")
        st.metric("Completed", completed)
    with col3:
        running = sum(1 for e in visible_events if e["state"] == "Running")
        st.metric("In Progress", running)
    with col4:
        avg_conf = sum(float(e["confidence"].rstrip("%")) for e in visible_events if e["confidence"] != "Not available") / len(visible_events)
        st.metric("Avg Confidence", f"{avg_conf:.1f}%")