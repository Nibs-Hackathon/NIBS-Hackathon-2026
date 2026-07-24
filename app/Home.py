import sys
from pathlib import Path
import asyncio
import platform
# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # app/ → project_root/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import importlib
import streamlit as st
import ui_helpers
if platform.system() == "Windows":
    # Fix for Windows connection reset errors
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print("✅ Windows asyncio fix applied (SelectorEventLoop)")
# Refresh shared UI helpers during Streamlit development reruns
importlib.reload(ui_helpers)

from ui_helpers import executive_metrics, metric_card, page_heading, render_sidebar, setup_page, status_chip
from app.frontend_services.backend_api_new import api
from services.simulator_controller import sim_controller
# In app/Home.py - add this after other imports
import importlib
import app.frontend_services.backend_api_new
importlib.reload(app.frontend_services.backend_api_new)
from components.global_notifications import render_global_notifications
import time


setup_page("Operations Center")
render_sidebar("Operations Center")
# ... imports ...


# ✅ RENDER GLOBAL NOTIFICATIONS (visible on Home page too)
render_global_notifications()

# ... rest of Home.py ...
if "notification_cleanup" not in st.session_state:
    st.session_state.notification_cleanup = time.time()

if time.time() - st.session_state.notification_cleanup > 5:
    st.session_state.notification_cleanup = time.time()
    st.rerun()

page_heading(
    "NIBS / AI OPERATIONS CENTER",
    "Welcome to Command Nexus",
    "A unified mission-control surface for operational intelligence, risk, and response."
)

# Add simulation controls to sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎮 Simulation Controls")

status = sim_controller.get_status()
st.sidebar.metric("Ticks", status['ticks'])
st.sidebar.metric("Events", status['events'])

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("▶️ Start", use_container_width=True):
        sim_controller.start()
        st.rerun()
with col2:
    if st.button("⏹️ Stop", use_container_width=True):
        sim_controller.stop()
        st.rerun()

if st.sidebar.button("⏭️ Step", use_container_width=True):
    telemetry, reports = sim_controller.step()
    st.sidebar.success(f"Step: {len(reports)} reports")

if st.sidebar.button("🔄 Refresh Config", use_container_width=True):
    api.refresh_config()
    st.sidebar.success("Config refreshed!")

st.sidebar.markdown("---")

left, right = st.columns([1.45, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>MISSION STATUS</div><h3 style='margin:.2rem 0 .6rem'>Operational picture: stable, with monitored assets.</h3><p class='muted'>Use the dashboard to review live health, incidents, agent decisions, and the current response queue.</p></div>", unsafe_allow_html=True)
with right:
    sim_status = "Running" if status.get("running") else "Stopped"
    st.markdown(f"<div class='panel'><div class='section-label'>PLATFORM STATUS</div>{status_chip(sim_status)}<p class='muted' style='margin-top:.8rem'>Demo workspace • {status['ticks']} ticks • {status['events']} events</p></div>", unsafe_allow_html=True)

st.write("")
st.markdown("<div class='section-label'>EXECUTIVE MISSION CONTROL</div>", unsafe_allow_html=True)
for metric_row in [executive_metrics()[:4], executive_metrics()[4:]]:
    for col, args in zip(st.columns(4), metric_row):
        with col:
            metric_card(*args)

st.write("")
st.markdown("<div class='panel'><div class='section-label'>QUICK START</div><p class='muted'>Navigate with the sidebar to inspect assets, simulate an incident, ask the global copilot, inspect predictive health, or review AI activity.</p></div>", unsafe_allow_html=True)