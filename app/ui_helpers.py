"""Shared presentation and placeholder-data utilities for the Streamlit UI.

This module deliberately has no backend imports so each page remains runnable while
the Operations Center integration layer is being designed.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from random import Random

import streamlit as st


COLORS = {
    "cyan": "#55D6FF",
    "violet": "#9B8CFF",
    "green": "#4FE3B2",
    "amber": "#FFBF69",
    "red": "#FF718D",
    "muted": "#8FA1BA",
}


def setup_page(title: str, icon: str = "◈") -> None:
    """Configure a page and apply the shared enterprise dark visual system."""
    st.set_page_config(page_title=f"{title} | NIBS Ops", page_icon=icon, layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background: radial-gradient(circle at 85% -10%, #182e52 0, #0b1220 34%, #070b13 72%); color: #e8f0ff; }
        [data-testid="stHeader"] { background: rgba(7, 11, 19, .78); backdrop-filter: blur(18px); }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #101b30 0%, #090f1d 100%); border-right: 1px solid rgba(123, 160, 207, .14); }
        [data-testid="stSidebar"] * { color: #dce8fa; }
        [data-testid="stSidebarNav"] { padding-top: .7rem; }
        [data-testid="stSidebarNav"] a { border-radius: 10px; margin: 2px 8px; padding: 8px 10px; }
        [data-testid="stSidebarNav"] a:hover { background: rgba(85,214,255,.10); }
        .ops-brand { font-size: .74rem; letter-spacing: .22em; color: #55d6ff; font-weight: 800; }
        .ops-title { font-size: 1.6rem; font-weight: 750; margin: .15rem 0 .1rem; color: #f4f8ff; }
        .ops-subtitle, .muted { color: #8fa1ba; }
        .section-label { color: #55d6ff; font-size: .72rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .25rem; }
        .metric-card { background: linear-gradient(145deg, rgba(25,42,70,.88), rgba(13,22,39,.88)); border: 1px solid rgba(129,172,226,.16); border-radius: 16px; padding: 1rem 1.1rem; min-height: 116px; box-shadow: 0 12px 32px rgba(0,0,0,.18); }
        .metric-card, .panel { transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease; backdrop-filter: blur(14px); }
        .metric-card:hover, .panel:hover { transform: translateY(-2px); border-color: rgba(85,214,255,.38); box-shadow: 0 16px 36px rgba(0,0,0,.24); }
        .metric-value { font-size: 1.65rem; font-weight: 760; color: #f5f8ff; margin: .15rem 0; }
        .metric-label { color: #9badc5; font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }
        .metric-delta { font-size: .78rem; font-weight: 650; }
        .panel { background: rgba(15,27,47,.76); border: 1px solid rgba(129,172,226,.14); border-radius: 15px; padding: 1rem 1.1rem; }
        .status { display: inline-block; border-radius: 999px; padding: .22rem .6rem; font-size: .72rem; font-weight: 750; letter-spacing: .04em; }
        .status-healthy, .status-running, .status-resolved { color:#6af0c2; background:rgba(79,227,178,.13); border:1px solid rgba(79,227,178,.3); }
        .status-warning, .status-pending { color:#ffd184; background:rgba(255,191,105,.13); border:1px solid rgba(255,191,105,.28); }
        .status-critical, .status-offline { color:#ff91a5; background:rgba(255,113,141,.13); border:1px solid rgba(255,113,141,.28); }
        .status-info { color:#8fe6ff; background:rgba(85,214,255,.13); border:1px solid rgba(85,214,255,.28); }
        .pulse { animation: pulse 1.8s ease-in-out infinite; } @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .38; } }
        .gauge { width: 128px; height: 128px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:.4rem auto; }
        .gauge-inner { width:98px; height:98px; border-radius:50%; background:#0d1728; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .timeline-row { display:grid; grid-template-columns:70px 24px 1fr; gap:10px; align-items:start; margin:.4rem 0; }
        .timeline-dot { width:13px; height:13px; border-radius:50%; background:#55d6ff; box-shadow:0 0 14px #55d6ff; margin-top:5px; }
        .twin-tile { min-height:172px; position:relative; overflow:hidden; }
        .stButton > button { border-radius: 9px; border: 1px solid rgba(85,214,255,.45); background: linear-gradient(135deg,#1686b8,#5664c9); color:#fff; font-weight:650; }
        .stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div { background:#101d31 !important; border-color:#284569 !important; color:#e8f0ff !important; }
        [data-testid="stDataFrame"] { border: 1px solid rgba(129,172,226,.14); border-radius: 12px; overflow: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(active: str) -> None:
    with st.sidebar:
        st.markdown("<div class='ops-brand'>NIBS • AI OPERATIONS</div>", unsafe_allow_html=True)
        st.markdown("<div class='ops-title'>Command Nexus</div>", unsafe_allow_html=True)
        st.caption("Industrial intelligence, unified.")
        st.divider()
        st.markdown("<div class='section-label'>Current workspace</div>", unsafe_allow_html=True)
        st.markdown(f"**{active}**")
        st.markdown("<span class='status status-running'>● SYSTEMS NOMINAL</span>", unsafe_allow_html=True)
        st.divider()
        st.caption("LIVE DEMO ENVIRONMENT")
        st.caption("Data shown is simulated until backend integration is enabled.")
        render_copilot_widget()


def render_copilot_widget() -> None:
    """Compact copilot that is intentionally available on every Streamlit page."""
    if "ops_messages" not in st.session_state:
        st.session_state.ops_messages = [{"role": "assistant", "content": "Command Nexus copilot online. Ask for an operational brief or recommendation."}]
    with st.sidebar.expander("✦ AI COPILOT", expanded=False):
        st.caption("Demo assistant • backend LLM connection pending")
        for message in st.session_state.ops_messages[-3:]:
            marker = "You" if message["role"] == "user" else "Nexus"
            st.caption(f"**{marker}:** {message['content']}")
        prompts = ["Summarize today's incidents", "Predict asset failures", "Explain system status", "Generate executive report", "Recommend maintenance"]
        prompt = st.selectbox("Suggested prompts", ["Select a prompt…"] + prompts, key="copilot_suggestion")
        typed = st.text_input("Ask Copilot", key="copilot_input", placeholder="Ask about operations")
        if st.button("Send", key="copilot_send", use_container_width=True):
            question = typed if typed.strip() else (prompt if prompt != "Select a prompt…" else "Explain system status")
            st.session_state.ops_messages.append({"role": "user", "content": question})
            st.session_state.ops_messages.append({"role": "assistant", "content": mock_copilot_response(question)})
            st.rerun()
    # TODO: Route messages, facility context, and conversation identity to the LLM/RAG backend.


def page_heading(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(f"<div class='section-label'>{eyebrow}</div><div class='ops-title'>{title}</div><div class='ops-subtitle'>{subtitle}</div>", unsafe_allow_html=True)
    st.write("")


def metric_card(label: str, value: str, delta: str, tone: str = "green") -> None:
    color = COLORS.get(tone, COLORS["green"])
    st.markdown(
        f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-delta' style='color:{color}'>{delta}</div></div>",
        unsafe_allow_html=True,
    )


def status_chip(status: str) -> str:
    key = status.lower().replace(" ", "-")
    return f"<span class='status status-{key}'>{status.upper()}</span>"


def mock_assets() -> list[dict]:
    return [
        {"Asset": "Pump A-01", "Type": "Centrifugal Pump", "Zone": "Process A", "Health": 96, "Status": "Healthy", "Last telemetry": "12 sec ago"},
        {"Asset": "Compressor C-12", "Type": "Gas Compressor", "Zone": "Process B", "Health": 82, "Status": "Warning", "Last telemetry": "18 sec ago"},
        {"Asset": "Tank T-04", "Type": "Storage Tank", "Zone": "Terminal", "Health": 91, "Status": "Healthy", "Last telemetry": "9 sec ago"},
        {"Asset": "Valve V-09", "Type": "Control Valve", "Zone": "Pipeline", "Health": 68, "Status": "Warning", "Last telemetry": "23 sec ago"},
        {"Asset": "Heat Exchanger H-03", "Type": "Heat Exchanger", "Zone": "Utilities", "Health": 43, "Status": "Critical", "Last telemetry": "31 sec ago"},
    ]


def mock_incidents() -> list[dict]:
    return [
        {"ID": "INC-2048", "Incident": "Elevated vibration", "Asset": "Compressor C-12", "Severity": "High", "Status": "Investigating", "Detected": "08:42"},
        {"ID": "INC-2047", "Incident": "Pressure variance", "Asset": "Valve V-09", "Severity": "Medium", "Status": "Monitoring", "Detected": "08:15"},
        {"ID": "INC-2046", "Incident": "Temperature excursion", "Asset": "Heat Exchanger H-03", "Severity": "Critical", "Status": "Escalated", "Detected": "07:51"},
    ]


def trend_series(points: int = 24, base: int = 88, spread: int = 6) -> dict[str, list[float]]:
    rng = Random(17)
    return {"Asset Health": [round(base + rng.uniform(-spread, spread), 1) for _ in range(points)], "Safety Index": [round(min(100, base + 4 + rng.uniform(-spread, spread)), 1) for _ in range(points)]}


def activity_items() -> list[tuple[str, str, str]]:
    return [
        ("08:42", "Diagnostic agent", "Started vibration root-cause analysis for Compressor C-12."),
        ("08:39", "Safety agent", "Validated operating envelope for Process B."),
        ("08:31", "Telemetry gateway", "Ingested 1,248 sensor readings across 42 assets."),
        ("08:15", "Workflow supervisor", "Closed INC-2043 with monitored recovery plan."),
    ]


def recent_dates(count: int = 6) -> list[str]:
    return [(datetime.now() - timedelta(days=index)).strftime("%d %b") for index in range(count - 1, -1, -1)]


def prediction_series(points: int = 14) -> dict[str, list[float]]:
    """Deterministic placeholder for projected health and intervention thresholds."""
    rng = Random(41)
    current = 84.0
    health = []
    for _ in range(points):
        current += rng.uniform(-2.8, -0.4)
        health.append(round(current, 1))
    return {"Predicted health": health, "Intervention threshold": [70.0] * points}


def mock_maintenance_tasks() -> list[dict]:
    return [
        {"Priority": "P1", "Asset": "Heat Exchanger H-03", "Work order": "Inspect thermal bypass", "Window": "Today · 14:00", "Owner": "Utilities Crew", "State": "Scheduled"},
        {"Priority": "P2", "Asset": "Compressor C-12", "Work order": "Bearing and vibration inspection", "Window": "Tomorrow · 09:00", "Owner": "Rotating Equipment", "State": "Proposed"},
        {"Priority": "P3", "Asset": "Valve V-09", "Work order": "Calibrate pressure actuator", "Window": "25 Jul · 11:00", "Owner": "Instrumentation", "State": "Planned"},
    ]


def mock_copilot_response(question: str) -> str:
    """Safe, deterministic stand-in for a future grounded LLM response."""
    lowered = question.lower()
    if "incident" in lowered:
        return "Three simulated incidents are open: one critical thermal excursion and two monitored asset anomalies. Heat Exchanger H-03 is the priority review."
    if "failure" in lowered or "predict" in lowered:
        return "Compressor C-12 has the strongest simulated failure signal: projected health is 68% in 14 days with a 32% failure probability."
    if "maintenance" in lowered:
        return "Prioritize Heat Exchanger H-03 today, then schedule Compressor C-12 bearing inspection for the next available rotating-equipment window."
    if "report" in lowered:
        return "Executive brief: mission status is stable with localized attention required in Utilities and Process B. Safety score remains 91.2/100."
    return "System status is stable: 42 of 45 assets are online, five AI agents are active, and incident workflows are being monitored in demo mode."


def executive_metrics() -> list[tuple[str, str, str, str]]:
    return [
        ("Overall health", "88.4%", "Within mission target", "green"),
        ("Active assets", "42 / 45", "3 under attention", "cyan"),
        ("AI agents", "6 / 6", "All online", "violet"),
        ("Open incidents", "03", "1 critical", "red"),
        ("Predicted failures", "02", "Next 14 days", "amber"),
        ("Safety score", "91.2", "Operating envelope secure", "green"),
        ("Mission status", "STABLE", "Monitored operations", "green"),
        ("System confidence", "94.6%", "Evidence quality high", "cyan"),
    ]


def mock_prediction_profile() -> dict:
    return {
        "health": 82,
        "rul": "43 days",
        "failure_probability": "32%",
        "confidence": "87%",
        "historical": {"Historical health": [96, 95, 95, 93, 92, 91, 90, 88, 87, 85, 84, 82]},
        "telemetry": [
            {"Signal": "Vibration RMS", "Observed": "23.7 mm/s", "Baseline": "15.0 mm/s", "Evidence": "Elevated +58%"},
            {"Signal": "Bearing temperature", "Observed": "78.2 °C", "Baseline": "68.0 °C", "Evidence": "Rising trend"},
            {"Signal": "Runtime since service", "Observed": "4,238 h", "Baseline": "3,600 h", "Evidence": "Past service window"},
        ],
    }


def mock_agent_timeline() -> list[dict]:
    return [
        {"time": "08:42:17", "agent": "Sensor Agent", "action": "Ingested vibration anomaly from Compressor C-12", "state": "Completed", "confidence": "99%", "progress": 100},
        {"time": "08:42:20", "agent": "Prediction Agent", "action": "Calculated 32% failure probability within 14 days", "state": "Completed", "confidence": "87%", "progress": 100},
        {"time": "08:42:25", "agent": "Knowledge Agent", "action": "Retrieved bearing inspection SOP and vibration limits", "state": "Completed", "confidence": "93%", "progress": 100},
        {"time": "08:42:31", "agent": "Planner Agent", "action": "Reserved next rotating-equipment maintenance window", "state": "Running", "confidence": "89%", "progress": 72},
        {"time": "08:42:37", "agent": "Notification Agent", "action": "Prepared operations escalation message", "state": "Queued", "confidence": "96%", "progress": 38},
        {"time": "08:42:42", "agent": "Report Agent", "action": "Compiling executive decision record", "state": "Queued", "confidence": "94%", "progress": 15},
    ]


def mock_twin_assets() -> list[dict]:
    return [
        {"Asset": "Pump A-01", "Category": "Pump", "Zone": "Process A", "Status": "Healthy", "Health": 96, "Temperature": "72 °C", "Pressure": "119 bar", "RPM": "2,960", "Failure": "4%"},
        {"Asset": "Motor M-07", "Category": "Motor", "Zone": "Process A", "Status": "Healthy", "Health": 93, "Temperature": "64 °C", "Pressure": "—", "RPM": "1,485", "Failure": "7%"},
        {"Asset": "Tank T-04", "Category": "Tank", "Zone": "Terminal", "Status": "Healthy", "Health": 91, "Temperature": "38 °C", "Pressure": "4.8 bar", "RPM": "—", "Failure": "9%"},
        {"Asset": "HVAC H-02", "Category": "HVAC", "Zone": "Utilities", "Status": "Warning", "Health": 76, "Temperature": "31 °C", "Pressure": "2.1 bar", "RPM": "1,120", "Failure": "18%"},
        {"Asset": "Generator G-01", "Category": "Generator", "Zone": "Utilities", "Status": "Healthy", "Health": 89, "Temperature": "79 °C", "Pressure": "6.2 bar", "RPM": "1,500", "Failure": "11%"},
        {"Asset": "Pipeline P-03", "Category": "Pipeline", "Zone": "Pipeline", "Status": "Warning", "Health": 68, "Temperature": "46 °C", "Pressure": "137 bar", "RPM": "—", "Failure": "24%"},
        {"Asset": "Compressor C-12", "Category": "Compressor", "Zone": "Process B", "Status": "Warning", "Health": 82, "Temperature": "78 °C", "Pressure": "112 bar", "RPM": "3,585", "Failure": "32%"},
    ]


def gauge_card(label: str, value: int, detail: str, color: str = "#55D6FF") -> None:
    st.markdown(
        f"<div class='panel' style='text-align:center'><div class='metric-label'>{label}</div><div class='gauge' style='background:conic-gradient({color} {value * 3.6}deg, #22344f 0)'><div class='gauge-inner'><b style='font-size:1.45rem'>{value}%</b><span class='muted' style='font-size:.7rem'>score</span></div></div><span class='muted'>{detail}</span></div>",
        unsafe_allow_html=True,
    )


def render_health_heatmap() -> None:
    """Compact CSS heatmap for the executive dashboard; data remains demo-only."""
    cells = [("Process A", "96%", "#4FE3B2"), ("Process B", "82%", "#FFBF69"), ("Terminal", "91%", "#4FE3B2"), ("Pipeline", "68%", "#FFBF69"), ("Utilities", "43%", "#FF718D")]
    blocks = "".join(f"<div style='flex:1;min-width:100px;padding:14px 10px;border-radius:11px;background:{color}20;border:1px solid {color}66'><b>{zone}</b><br><span style='font-size:1.45rem;color:{color}'>{score}</span></div>" for zone, score, color in cells)
    st.markdown(f"<div style='display:flex;gap:10px;flex-wrap:wrap'>{blocks}</div>", unsafe_allow_html=True)
