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
        .metric-value { font-size: 1.65rem; font-weight: 760; color: #f5f8ff; margin: .15rem 0; }
        .metric-label { color: #9badc5; font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }
        .metric-delta { font-size: .78rem; font-weight: 650; }
        .panel { background: rgba(15,27,47,.76); border: 1px solid rgba(129,172,226,.14); border-radius: 15px; padding: 1rem 1.1rem; }
        .status { display: inline-block; border-radius: 999px; padding: .22rem .6rem; font-size: .72rem; font-weight: 750; letter-spacing: .04em; }
        .status-healthy, .status-running, .status-resolved { color:#6af0c2; background:rgba(79,227,178,.13); border:1px solid rgba(79,227,178,.3); }
        .status-warning, .status-pending { color:#ffd184; background:rgba(255,191,105,.13); border:1px solid rgba(255,191,105,.28); }
        .status-critical, .status-offline { color:#ff91a5; background:rgba(255,113,141,.13); border:1px solid rgba(255,113,141,.28); }
        .status-info { color:#8fe6ff; background:rgba(85,214,255,.13); border:1px solid rgba(85,214,255,.28); }
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
