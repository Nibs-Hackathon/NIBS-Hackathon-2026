import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from frontend_services.maintenance_adapter import get_maintenance_plan
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip
from components.global_notifications import render_global_notifications

setup_page("Maintenance Planner")
render_sidebar("Maintenance Planner")
render_global_notifications()

page_heading(
    "🔧 WORK ORCHESTRATION",
    "Maintenance Planner",
    "Turn MAO task state and recommendations into an executable maintenance view.",
)

plan = get_maintenance_plan()

# ✅ If no tasks, show a way to generate them
if not plan.get("tasks"):
    st.info("No maintenance tasks have been generated yet. Trigger an incident to generate tasks.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚨 Generate Pressure Incident", use_container_width=True):
            from frontend_services.incident_adapter import trigger_incident
            result = trigger_incident("pressure spike")
            st.success("✅ Incident triggered! Refreshing...")
            st.rerun()
    with col2:
        if st.button("🌡️ Generate Temperature Incident", use_container_width=True):
            from frontend_services.incident_adapter import trigger_incident
            result = trigger_incident("high temperature")
            st.success("✅ Incident triggered! Refreshing...")
            st.rerun()
    with col3:
        if st.button("💨 Generate Gas Leak", use_container_width=True):
            from frontend_services.incident_adapter import trigger_incident
            result = trigger_incident("gas leak")
            st.success("✅ Incident triggered! Refreshing...")
            st.rerun()
    
    st.stop()

# ✅ Display metrics
for col, args in zip(st.columns(4), plan.get("metrics", [])):
    with col:
        metric_card(*args)

st.write("")

# ✅ Main view
left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>📋 RECOMMENDED WORK PLAN</div>", unsafe_allow_html=True)
    
    # ✅ Convert to dataframe for better display
    df = pd.DataFrame(plan["tasks"])
    
    # ✅ Add color coding
    def color_priority(val):
        if val == "P1":
            return "color: #ff718d; font-weight: bold;"
        elif val == "P2":
            return "color: #ffbf69; font-weight: bold;"
        else:
            return "color: #4fe3b2;"
    
    def color_state(val):
        if val == "Completed":
            return "color: #4fe3b2;"
        elif val == "In Progress":
            return "color: #ffbf69;"
        else:
            return "color: #8fa1ba;"
    
    # ✅ Apply styling
    styled_df = df.style.applymap(color_priority, subset=["Priority"])
    styled_df = styled_df.applymap(color_state, subset=["State"])
    
    st.dataframe(styled_df, hide_index=True, height=300, use_container_width=True)

with right:
    st.markdown("<div class='section-label'>📊 PLANNING STATUS</div>", unsafe_allow_html=True)
    
    st.metric("Latest priority", plan.get("priority", "N/A"))
    st.metric("Estimated downtime", plan.get("downtime", "N/A"))
    
    # ✅ Task count by priority
    if plan["tasks"]:
        priorities = [t["Priority"] for t in plan["tasks"]]
        p1_count = priorities.count("P1")
        p2_count = priorities.count("P2")
        p3_count = priorities.count("P3")
        
        st.markdown(f"""
        <div style="margin-top: 16px; padding: 12px; background: rgba(13,23,40,0.4); border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="color: #ff718d;">🔴 Critical (P1)</span>
                <span style="font-weight: 600; color: #ff718d;">{p1_count}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="color: #ffbf69;">🟠 High (P2)</span>
                <span style="font-weight: 600; color: #ffbf69;">{p2_count}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #4fe3b2;">🟢 Low (P3)</span>
                <span style="font-weight: 600; color: #4fe3b2;">{p3_count}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ✅ Timeline view
left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>⏱️ MAINTENANCE TIMELINE</div>", unsafe_allow_html=True)
    
    # ✅ Instead of using applymap (which doesn't exist on Styler), use a simpler approach

    if plan["tasks"]:
        df = pd.DataFrame(plan["tasks"])
        
        # ✅ Simple display without complex styling
        st.dataframe(df, hide_index=True, height=300, use_container_width=True)
    else:
        st.info("No MAO maintenance tasks have been generated yet.")

with right:
    st.markdown("<div class='section-label'>🤖 AI SCHEDULING RATIONALE</div>", unsafe_allow_html=True)
    
    if plan.get("rationale"):
        st.markdown(
            """
            <div class='panel' style="max-height: 400px; overflow-y: auto;">
                <b>Latest MAO recommendations</b>
                <ul style="margin-top: 8px; padding-left: 20px;">
            """
            + "".join(f"<li style='margin: 6px 0; color: #c0d0e8;'>{item}</li>" for item in plan["rationale"][:10])
            + """
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No planning-agent recommendation is available yet.")
    
    st.write("")
    
    # ✅ Quick actions
    st.markdown("<div class='section-label'>⚡ QUICK ACTIONS</div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Tasks", use_container_width=True):
        st.rerun()
    if st.button("📊 Export Schedule", use_container_width=True):
        st.info("Export functionality coming soon.")