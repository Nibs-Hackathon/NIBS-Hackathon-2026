# Folder: app Code Inventory

Generated: 2026-07-23 12:30:25 UTC

Contains 25 project files.

## app/components/__init__.py

**File path:** `app/components/__init__.py`

```python
"""Reusable Streamlit presentation components for the RigOS frontend."""
```

## app/components/agent_card.py

**File path:** `app/components/agent_card.py`

```python
import streamlit as st


def render_agent_card(report):

    text = report.final_summary.lower()

    if "[safety]" in text:
        agent_name = "🛡 Safety Agent"

    elif "[diagnostic]" in text:
        agent_name = "🔍 Diagnostic Agent"

    elif "[knowledge]" in text:
        agent_name = "📚 Knowledge Agent"

    else:
        agent_name = "🤖 AI Agent"


    cleaned = (
        report.final_summary
        .replace("[safety]", "")
        .replace("[diagnostic]", "")
        .replace("[knowledge]", "")
    )


    st.markdown(
        f"""
        <div class="agent-card">

        <h3>{agent_name}</h3>

        <p>
        {cleaned}
        </p>

        <b>Status:</b> Completed ✅

        </div>
        """,
        unsafe_allow_html=True
    )
```

## app/components/incident_card.py

**File path:** `app/components/incident_card.py`

```python
import streamlit as st


def render_incident_card(
    asset,
    incident_type,
    severity,
    status="Processing"
):

    st.markdown(
        f"""
        <div class="incident-card">

        <h2>🚨 {incident_type}</h2>

        <p>
        <b>Asset:</b> {asset}
        </p>

        <p>
        <b>Severity:</b>
        <span style="color:#ff5555">
        {severity}
        </span>
        </p>

        <p>
        <b>Status:</b> {status}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
```

## app/components/investigation_progress.py

**File path:** `app/components/investigation_progress.py`

```python
import streamlit as st


def render_investigation_progress():
    st.markdown("### 🤖 AI Investigation")

    stages = [
        ("🛡 Safety Analysis", "Completed"),
        ("🔍 Diagnostic Analysis", "Completed"),
        ("📚 Knowledge Retrieval", "Completed"),
        ("🔧 Maintenance Review", "Completed"),
        ("📋 Planning", "Completed"),
    ]

    for stage, status in stages:
        left, right = st.columns([5, 1])

        with left:
            st.write(stage)

        with right:
            st.success(status)
```

## app/components/phase_one_views.py

**File path:** `app/components/phase_one_views.py`

```python
"""Reusable Phase 1 visual components.

These components are presentation-only. They accept data supplied by the page
or frontend helpers and never create a MAO kernel or call backend services.
"""

from __future__ import annotations

import streamlit as st

from ui_helpers import status_chip


def render_live_signal_banner(label: str, detail: str, status: str = "Running") -> None:
    """Render a compact operational status banner."""
    st.markdown(
        f"<div class='panel'><span class='pulse' style='color:#4FE3B2'>●</span> "
        f"<b>{label}</b> &nbsp; {status_chip(status)}"
        f"<br><span class='muted'>{detail}</span></div>",
        unsafe_allow_html=True,
    )


def render_incident_response_flow(steps: list[tuple[str, str]]) -> None:
    """Visualize the existing incident-to-report demo lifecycle without executing it."""
    st.markdown("<div class='section-label'>RESPONSE LIFECYCLE</div>", unsafe_allow_html=True)
    for index, (title, detail) in enumerate(steps, start=1):
        st.markdown(
            f"<div class='timeline-row'><span class='muted'>STEP {index}</span>"
            f"<span class='timeline-dot'></span><div class='panel'><b>{title}</b>"
            f"<br><span class='muted'>{detail}</span></div></div>",
            unsafe_allow_html=True,
        )


def render_agent_execution_view(agents: list[dict]) -> None:
    """Render registered/demo agent state as a vertical command-center flow."""
    st.markdown("<div class='section-label'>AGENT EXECUTION VIEW</div>", unsafe_allow_html=True)
    for agent in agents:
        state = agent["State"]
        state_tone = "Running" if state == "Active" else ("Pending" if state == "Queued" else "Info")
        pulse_class = "pulse" if state == "Active" else ""
        st.markdown(
            f"<div class='timeline-row'><span class='muted'>{agent['Specialty']}</span>"
            f"<span class='timeline-dot {pulse_class}'></span><div class='panel'>"
            f"<b>{agent['Agent']} Agent</b> &nbsp; {status_chip(state_tone)}"
            f"<br><span class='muted'>{agent['Current task']} · Confidence {agent['Confidence']}</span>"
            f"</div></div>",
            unsafe_allow_html=True,
        )
```

## app/components/phase_two_views.py

**File path:** `app/components/phase_two_views.py`

```python
"""Reusable presentation components for Phase 2 frontend pages."""

from __future__ import annotations

import streamlit as st

from ui_helpers import status_chip


def render_asset_detail_panel(asset: dict, sensors: list[dict]) -> None:
    """Show selected asset condition and its current demo telemetry snapshot."""
    st.markdown("<div class='section-label'>SELECTED ASSET DETAIL</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='panel'><b>{asset['Asset']}</b> &nbsp; {status_chip(asset['Status'])}"
        f"<p class='muted'>{asset['Type']} · {asset['Zone']}<br>"
        f"Health: {asset['Health']}% · Last telemetry: {asset['Last telemetry']}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>SENSOR SNAPSHOT</div>", unsafe_allow_html=True)
    st.dataframe(sensors, hide_index=True, use_container_width=True)


def render_report_detail_panel(report: dict) -> None:
    """Render the current report preview in a reusable glass panel."""
    st.markdown(
        f"<div class='panel'><b>{report['Report']} · {report['Title']}</b>"
        f"<p class='muted'>{report['Summary']}</p>"
        f"<p><b>Recommendation:</b> {report['Recommendation']}</p></div>",
        unsafe_allow_html=True,
    )


def render_copilot_context_panel() -> None:
    """Shared visual context for the full-page Copilot workspace."""
    st.markdown("<div class='section-label'>CONTEXT IN USE</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><b>Demo facility</b><p class='muted'>RigOS Alpha Refinery</p>"
        "<b>Priority signal</b><p class='muted'>Compressor C-12 vibration watch</p>"
        "<b>Knowledge mode</b><p class='muted'>Simulated SOP retrieval</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>SUGGESTED PROMPTS</div>", unsafe_allow_html=True)
    st.caption("• Summarize today's incidents\n\n• Predict asset failures\n\n• Explain system status\n\n• Generate executive report\n\n• Recommend maintenance")
```

## app/components/telemetry_card.py

**File path:** `app/components/telemetry_card.py`

```python
import streamlit as st


def render_telemetry():

    st.markdown("### 📊 Live Telemetry")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Pressure</div>
                <div class="metric-value">152 PSI</div>
                <div class="status status-critical">HIGH</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Temperature</div>
                <div class="metric-value">84 °C</div>
                <div class="status status-warning">ELEVATED</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Flow Rate</div>
                <div class="metric-value">310 L/min</div>
                <div class="status status-running">NORMAL</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">AI Status</div>
                <div class="metric-value">Running</div>
                <div class="status status-info">ACTIVE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
```

## app/components/timeline.py

**File path:** `app/components/timeline.py`

```python
import streamlit as st


def render_timeline():
    st.markdown("### ⏱ Incident Timeline")

    events = [
        ("10:42:01", "🚨 Pressure spike detected"),
        ("10:42:03", "🛡 Safety Agent executed"),
        ("10:42:05", "🔍 Diagnostic completed"),
        ("10:42:08", "📚 Knowledge retrieved"),
        ("10:42:10", "🔧 Maintenance recommended"),
        ("10:42:12", "📋 Planning completed"),
    ]

    for time, event in events:
        st.markdown(
            f"""
            <div class="timeline-row">
                <div style="color:#8fa1ba;font-size:0.9rem;">{time}</div>
                <div class="timeline-dot"></div>
                <div>{event}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
```

## app/frontend_services/__init__.py

**File path:** `app/frontend_services/__init__.py`

```python
"""Frontend-facing adapters for existing RigOS backend modules."""
```

## app/frontend_services/knowledge_agent_adapter.py

**File path:** `app/frontend_services/knowledge_agent_adapter.py`

```python
"""Frontend routing for Command Nexus conversational and operational requests."""

from __future__ import annotations

from functools import lru_cache
import logging
from pathlib import Path
import re
import sys
from typing import TYPE_CHECKING, Callable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if TYPE_CHECKING:
    from agents.knowledge import KnowledgeAgent


LOGGER = logging.getLogger(__name__)
ProgressCallback = Callable[[str], None]

OPERATIONAL_KEYWORDS = (
    "asset", "compressor", "pump", "pipeline", "tank", "valve", "maintenance",
    "inspection", "incident", "alarm", "safety", "hazard", "pressure",
    "temperature", "vibration", "flow", "gas", "refinery", "sop", "procedure",
    "equipment", "motor", "turbine", "boiler", "heat exchanger", "reactor",
    "distillation", "column", "flare", "corrosion", "shutdown", "startup",
    "trip", "failure", "process", "telemetry", "sensor",
)


def is_operational_query(question: str) -> bool:
    """Return whether a question requires the refinery operations path."""
    normalized = re.sub(r"\s+", " ", question.strip().casefold())
    return bool(normalized and any(keyword in normalized for keyword in OPERATIONAL_KEYWORDS))


def generate_conversational_response(question: str) -> str:
    """Use Gemini for casual conversation without starting the operational path."""
    from services.llm import LLMManager

    prompt = f"""
You are Command Nexus, a polished industrial operations copilot.

Reply naturally to this casual user message: {question!r}

Keep the response concise, warm, and professional. You may introduce yourself
as an industrial operations copilot and offer help with refinery operations,
equipment, maintenance, incident response, and safety. Do not provide
operational facts, citations, or technical instructions for a casual message.
Never mention implementation, search, retrieval, documents, a knowledge base,
databases, RAG, prompts, APIs, or model internals.
"""
    return LLMManager().generate(prompt)


def _emit(callback: ProgressCallback | None, message: str) -> None:
    """Log and optionally expose a diagnostic stage without changing backend behavior."""
    LOGGER.info(message)
    if callback is not None:
        callback(message)


class KnowledgeAgentUnavailable(RuntimeError):
    """Raised when the existing backend knowledge path cannot serve a query."""


@lru_cache(maxsize=1)
def get_knowledge_agent() -> "KnowledgeAgent":
    """Initialize the existing agent once per Streamlit server process."""
    try:
        from agents.knowledge import KnowledgeAgent

        return KnowledgeAgent()
    except Exception as error:
        raise KnowledgeAgentUnavailable("Command Nexus is temporarily unavailable. Please try again shortly.") from error


def ask_knowledge_agent(question: str, on_progress: ProgressCallback | None = None) -> str:
    """Route casual conversation to Gemini and operational questions to KnowledgeAgent."""
    _emit(on_progress, "Command Nexus received a question.")
    normalized_question = question.strip()
    if not normalized_question:
        raise KnowledgeAgentUnavailable("Enter a question before asking Command Nexus.")

    if not is_operational_query(normalized_question):
        _emit(on_progress, "Conversational request detected.")
        try:
            return generate_conversational_response(normalized_question)
        except Exception as error:
            LOGGER.exception("Command Nexus conversational response failed")
            raise KnowledgeAgentUnavailable(
                "Command Nexus is temporarily unavailable. Please try again shortly."
            ) from error

    _emit(on_progress, "Preparing an operational assessment.")
    try:
        # Backend imports are lazy so ordinary Streamlit rendering does not
        # initialize the operational stack until an operational question arrives.
        from mao.models.task import Task

        task = Task(
            name="Operator knowledge query",
            description=normalized_question,
            assigned_agent="knowledge",
        )
        agent = get_knowledge_agent()
        result = agent.execute(task)
    except KnowledgeAgentUnavailable:
        raise
    except Exception as error:
        LOGGER.exception("Command Nexus operational response failed")
        raise KnowledgeAgentUnavailable(
            "Command Nexus is temporarily unavailable. Please try again shortly."
        ) from error

    if not result.success or not result.summary:
        raise KnowledgeAgentUnavailable("Command Nexus could not prepare an operational assessment. Please try again.")

    _emit(on_progress, "Operational assessment prepared.")
    return result.summary
```

## app/Home.py

**File path:** `app/Home.py`

```python
import importlib

import streamlit as st
import ui_helpers

# Refresh shared UI helpers during Streamlit development reruns so an older
# module cached by the script runner cannot mask newly added components.
importlib.reload(ui_helpers)

from ui_helpers import executive_metrics, metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Operations Center")
render_sidebar("Operations Center")
page_heading("NIBS / AI OPERATIONS CENTER", "Welcome to Command Nexus", "A unified mission-control surface for operational intelligence, risk, and response.")

left, right = st.columns([1.45, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>MISSION STATUS</div><h3 style='margin:.2rem 0 .6rem'>Operational picture: stable, with two monitored assets.</h3><p class='muted'>Use the dashboard to review live health, incidents, agent decisions, and the current response queue.</p></div>", unsafe_allow_html=True)
with right:
    st.markdown(f"<div class='panel'><div class='section-label'>PLATFORM STATUS</div>{status_chip('Running')}<p class='muted' style='margin-top:.8rem'>Demo workspace • Simulated telemetry</p></div>", unsafe_allow_html=True)

st.write("")
st.markdown("<div class='section-label'>EXECUTIVE MISSION CONTROL</div>", unsafe_allow_html=True)
for metric_row in [executive_metrics()[:4], executive_metrics()[4:]]:
    for col, args in zip(st.columns(4), metric_row):
        with col:
            metric_card(*args)

st.write("")
st.markdown("<div class='panel'><div class='section-label'>QUICK START</div><p class='muted'>Navigate with the sidebar to inspect assets, simulate an incident, ask the global copilot, inspect predictive health, or review AI activity.</p></div>", unsafe_allow_html=True)
```

## app/pages/1_Dashboard.py

**File path:** `app/pages/1_Dashboard.py`

```python
import streamlit as st
from components.phase_one_views import render_live_signal_banner
from ui_helpers import dashboard_demo_snapshot, metric_card, page_heading, render_health_heatmap, render_sidebar, setup_page, trend_series

setup_page("Dashboard")
render_sidebar("Executive Dashboard")
page_heading("OVERVIEW", "Operations Dashboard", "Real-time operational intelligence across the facility.")
snapshot = dashboard_demo_snapshot()
render_live_signal_banner("LIVE DEMO TELEMETRY", "Operational data shown is the existing frontend demo snapshot. Backend stream integration is pending.")
st.write("")

for col, args in zip(st.columns(4), snapshot["metrics"]):
    with col: metric_card(*args)

st.write("")
st.markdown("<div class='section-label'>FACILITY HEALTH HEATMAP</div>", unsafe_allow_html=True)
render_health_heatmap()
st.write("")
left, right = st.columns([1.65, 1])
with left:
    st.markdown("<div class='section-label'>24-HOUR OPERATIONAL HEALTH</div>", unsafe_allow_html=True)
    st.line_chart(trend_series(), color=["#55D6FF", "#9B8CFF"], height=280)
with right:
    st.markdown("<div class='section-label'>ATTENTION QUEUE</div>", unsafe_allow_html=True)
    for item in snapshot["incidents"]:
        st.markdown(f"<div class='panel'><b>{item['Incident']}</b><br><span class='muted'>{item['Asset']} • {item['Severity']} • {item['Detected']}</span></div>", unsafe_allow_html=True)
        st.write("")

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>ASSET WATCHLIST</div>", unsafe_allow_html=True)
    st.dataframe(snapshot["assets"], hide_index=True, use_container_width=True, height=245)
with right:
    st.markdown("<div class='section-label'>LIVE ACTIVITY</div>", unsafe_allow_html=True)
    for time, actor, text in snapshot["activity"]:
        st.markdown(f"**{time} · {actor}**  \n<span class='muted'>{text}</span>", unsafe_allow_html=True)
```

## app/pages/10_Health_Prediction.py

**File path:** `app/pages/10_Health_Prediction.py`

```python
import streamlit as st

from ui_helpers import gauge_card, metric_card, mock_prediction_profile, page_heading, prediction_series, render_sidebar, setup_page


setup_page("Health Prediction")
render_sidebar("Predictive Health")
page_heading("PREDICTIVE INTELLIGENCE", "Asset Health Prediction", "Forecast degradation risk early enough to plan safe, efficient intervention.")

assets = ["Compressor C-12", "Heat Exchanger H-03", "Valve V-09", "Pump A-01"]
profile = mock_prediction_profile()
left, right = st.columns([1, 1.5])
with left:
    asset = st.selectbox("Forecast asset", assets)
    horizon = st.select_slider("Forecast horizon", options=["7 days", "14 days", "30 days"], value="14 days")
    st.markdown("<div class='panel'><div class='section-label'>MODEL STATUS</div><b>Forecast engine: demo mode</b><p class='muted'>Placeholder projections are displayed until telemetry-history and model endpoints are exposed.</p></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>PROJECTED HEALTH · " + asset.upper() + "</div>", unsafe_allow_html=True)
    st.line_chart(prediction_series(), color=["#55D6FF", "#FFBF69"], height=280)

gauge_columns = st.columns(3)
with gauge_columns[0]:
    gauge_card("Health score", profile["health"], "Current modeled condition", "#55D6FF")
with gauge_columns[1]:
    gauge_card("Model confidence", 87, "Evidence consistency", "#4FE3B2")
with gauge_columns[2]:
    gauge_card("Failure risk", 32, "14-day probability", "#FF718D")

for col, args in zip(st.columns(4), [("Current health", f"{profile['health']}%", "Watch threshold: 80%", "amber"), ("Remaining useful life", profile["rul"], "Estimate before intervention", "cyan"), ("Failure probability", profile["failure_probability"], f"At end of {horizon}", "red"), ("Model confidence", profile["confidence"], "Sufficient evidence", "green")]):
    with col:
        metric_card(*args)

st.write("")
left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>HISTORICAL HEALTH TIMELINE</div>", unsafe_allow_html=True)
    st.line_chart(profile["historical"], color="#4FE3B2", height=210)
with right:
    st.markdown("<div class='section-label'>AI DECISION EXPLANATION</div><div class='panel'><b>Why this prediction was made</b><p class='muted'>Vibration and bearing temperature have increased while runtime has exceeded the expected service window.</p><b>Recommended action</b><p class='muted'>Schedule bearing inspection within six days and reduce load if vibration rises further.</p><b>Expected impact</b><p class='muted'>Avoid an estimated 18 hours of unplanned downtime.</p></div>", unsafe_allow_html=True)

st.markdown("<div class='section-label'>SUPPORTING TELEMETRY</div>", unsafe_allow_html=True)
st.dataframe(profile["telemetry"], hide_index=True, use_container_width=True)

# TODO: Replace prediction_series with backend model forecasts based on live telemetry and service history.
```

## app/pages/11_Maintenance_Planner.py

**File path:** `app/pages/11_Maintenance_Planner.py`

```python
import streamlit as st

from ui_helpers import metric_card, mock_maintenance_tasks, page_heading, render_sidebar, setup_page, status_chip


setup_page("Maintenance Planner")
render_sidebar("Maintenance Planner")
page_heading("WORK ORCHESTRATION", "Maintenance Planner", "Turn asset risk and AI recommendations into an executable maintenance plan.")

for col, args in zip(st.columns(4), [("Planned work", "12", "Across 4 crews", "cyan"), ("High priority", "02", "Needs today", "red"), ("Schedule load", "76%", "Within capacity", "green"), ("Predicted avoided risk", "18%", "Next 30 days", "violet")]):
    with col:
        metric_card(*args)

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>RECOMMENDED WORK PLAN</div>", unsafe_allow_html=True)
    st.dataframe(mock_maintenance_tasks(), hide_index=True, use_container_width=True, height=250)
with right:
    st.markdown("<div class='section-label'>PLANNING CONTROLS</div>", unsafe_allow_html=True)
    st.selectbox("Planning window", ["Next 7 days", "Next 14 days", "Next 30 days"])
    st.selectbox("Crew availability", ["All crews", "Rotating Equipment", "Utilities Crew", "Instrumentation"])
    st.button("Generate AI work plan", use_container_width=True)
    st.button("Balance schedule", use_container_width=True)
    st.caption("These controls are UI-only in the current prototype.")

st.write("")
left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>MAINTENANCE TIMELINE</div>", unsafe_allow_html=True)
    timeline = [("Today · 14:00", "Heat Exchanger H-03", "Utilities Crew", "P1", "2.5 h"), ("Tomorrow · 09:00", "Compressor C-12", "Rotating Equipment", "P2", "4.0 h"), ("25 Jul · 11:00", "Valve V-09", "Instrumentation", "P3", "1.5 h")]
    for window, asset, engineer, priority, downtime in timeline:
        st.markdown(f"<div class='timeline-row'><span class='muted'>{window}</span><span class='timeline-dot'></span><div class='panel'><b>{asset}</b> &nbsp; {status_chip('Critical' if priority == 'P1' else 'Warning')}<br><span class='muted'>Assigned engineer: {engineer} · Estimated downtime: {downtime}</span></div></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>AI SCHEDULING RATIONALE</div><div class='panel'><b>Optimized sequence</b><p class='muted'>Prioritizes the thermal-risk work order ahead of compressor inspection, while grouping pipeline work with instrumentation availability.</p><b>Expected impact</b><p class='muted'>Reduces forecasted operational risk by 18% and avoids overlap with peak production windows.</p></div>", unsafe_allow_html=True)

# TODO: Persist maintenance tasks, crew capacity, work-order status, and planning decisions through backend APIs.
```

## app/pages/12_AI_Activity.py

**File path:** `app/pages/12_AI_Activity.py`

```python
import streamlit as st

from ui_helpers import metric_card, mock_agent_timeline, page_heading, render_sidebar, setup_page, status_chip


setup_page("AI Activity")
render_sidebar("AI Activity Timeline")
page_heading("AUTONOMY AUDIT", "AI Agent Activity Timeline", "A chronological, reviewable record of AI observation, reasoning, and workflow handoffs.")

for col, args in zip(st.columns(4), [("Activities today", "386", "+14% from yesterday", "cyan"), ("Completed workflows", "34", "No failed executions", "green"), ("Human reviews", "08", "2 awaiting review", "amber"), ("Avg. confidence", "94.6%", "Governance target met", "violet")]):
    with col:
        metric_card(*args)

st.write("")
filter_col, search_col = st.columns([1, 2])
with filter_col:
    st.selectbox("Agent", ["All agents", "Safety", "Diagnostic", "Knowledge", "Maintenance", "Planning"])
with search_col:
    st.text_input("Search activity", placeholder="Filter by asset, workflow, or action")

st.markdown("<div class='section-label'>LIVE EXECUTION FLOW</div>", unsafe_allow_html=True)
for event in mock_agent_timeline():
    state_tone = "Running" if event["state"] == "Running" else ("Pending" if event["state"] == "Queued" else "Info")
    st.markdown(f"<div class='timeline-row'><span class='muted'>{event['time']}</span><span class='timeline-dot {'pulse' if event['state'] == 'Running' else ''}'></span><div class='panel'><b>{event['agent']}</b> &nbsp; {status_chip(state_tone)}<br><span class='muted'>{event['action']} · Confidence {event['confidence']}</span></div></div>", unsafe_allow_html=True)
    st.progress(event["progress"], text=f"{event['progress']}% execution progress")

# TODO: Read immutable agent lifecycle events and audit metadata from the MAO backend/event store.
```

## app/pages/13_Digital_Twin.py

**File path:** `app/pages/13_Digital_Twin.py`

```python
import streamlit as st

from ui_helpers import mock_twin_assets, page_heading, render_sidebar, setup_page, status_chip


setup_page("Digital Twin")
render_sidebar("Digital Twin")
page_heading("FACILITY TOPOLOGY", "Digital Twin View", "A live-ready operational map of facility zones, asset condition, and active process signals.")

st.info("Digital twin is running in visual-demo mode. Asset positions and signals are simulated.")

assets = mock_twin_assets()
selected_name = st.selectbox("Inspect digital-twin asset", [asset["Asset"] for asset in assets])
selected = next(asset for asset in assets if asset["Asset"] == selected_name)

st.markdown("<div class='section-label'>INTERACTIVE FACILITY LAYERS</div>", unsafe_allow_html=True)
columns = st.columns(4)
for col, asset in zip(columns * 2, assets):
    with col:
        st.markdown(f"<div class='panel twin-tile'><div class='section-label'>{asset['Zone']} · {asset['Category']}</div><b>{asset['Asset']}</b><p style='margin:.7rem 0'>{status_chip(asset['Status'])}</p><p class='muted'>Health: {asset['Health']}%<br>Temp: {asset['Temperature']} · Pressure: {asset['Pressure']}<br>RPM: {asset['RPM']} · Failure: {asset['Failure']}</p></div>", unsafe_allow_html=True)

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown("<div class='section-label'>PROCESS CONNECTIONS</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel' style='text-align:center; padding:2rem'><b>PROCESS A</b> &nbsp; ───► &nbsp; <b>PROCESS B</b> &nbsp; ───► &nbsp; <b>TERMINAL</b><br><br><span class='muted'>Utilities support all zones · Pipeline transfer monitored continuously</span></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>SELECTED ASSET DETAIL</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'><b>{selected['Asset']}</b><p>{status_chip(selected['Status'])}</p><span class='muted'>Health: {selected['Health']}%<br>Temperature: {selected['Temperature']}<br>Pressure: {selected['Pressure']}<br>RPM: {selected['RPM']}<br>Failure probability: {selected['Failure']}</span><hr><b>AI recommendation</b><p class='muted'>Continue monitoring. Escalate if the live failure probability exceeds the configured threshold.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>TWIN CONTROLS</div>", unsafe_allow_html=True)
    st.selectbox("Overlay", ["Asset health", "Live telemetry", "Incident severity", "Maintenance schedule"])
    st.toggle("Show process connections", value=True)
    st.toggle("Highlight active incidents", value=True)

# TODO: Bind zones, topology, asset coordinates, and live sensor overlays to a backend digital-twin data source.
```

## app/pages/2_Assets.py

**File path:** `app/pages/2_Assets.py`

```python
import streamlit as st
from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_asset_detail_panel
from ui_helpers import asset_monitor_demo_snapshot, metric_card, page_heading, render_sidebar, setup_page, trend_series

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")
page_heading("FLEET INTELLIGENCE", "Asset Monitoring", "Health, telemetry, and operational posture for every connected asset.")
render_live_signal_banner("ASSET DEMO SNAPSHOT", "The existing asset and telemetry demo is isolated for future state-manager integration.", "Info")
st.write("")

snapshot = asset_monitor_demo_snapshot()
assets = snapshot["assets"]
filters = st.columns(3)
with filters[0]: zone = st.selectbox("Zone", ["All zones", "Process A", "Process B", "Terminal", "Pipeline", "Utilities"])
with filters[1]: status = st.selectbox("Status", ["All statuses", "Healthy", "Warning", "Critical"])
with filters[2]: selected = st.selectbox("Focus asset", [a["Asset"] for a in assets])

# TODO: Replace asset_monitor_demo_snapshot with a read-only asset/telemetry adapter.
visible = [a for a in assets if (zone == "All zones" or a["Zone"] == zone) and (status == "All statuses" or a["Status"] == status)]
st.dataframe(visible, hide_index=True, use_container_width=True, height=260)

st.write("")
for col, args in zip(st.columns(4), [("Selected asset", selected, "Telemetry connected", "cyan"), ("Current health", "82%", "Watch threshold: 80%", "amber"), ("Sensor coverage", "5 / 5", "All channels reporting", "green"), ("Last update", "18 sec", "Within SLA", "green")]):
    with col: metric_card(*args)

left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>HEALTH & SAFETY TREND</div>", unsafe_allow_html=True)
    st.line_chart(trend_series(18, 84, 8), color=["#55D6FF", "#4FE3B2"], height=260)
with right:
    selected_asset = next(asset for asset in assets if asset["Asset"] == selected)
    render_asset_detail_panel(selected_asset, snapshot["sensors"])
```

## app/pages/3_Control_Center.py

**File path:** `app/pages/3_Control_Center.py`

```python
import streamlit as st
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip

setup_page("Control Center")
render_sidebar("Control Center")
page_heading("MISSION CONTROL", "Control Center", "A protected command surface for supervising facility-level operating state.")

for col, args in zip(st.columns(4), [("Facility mode", "RUNNING", "Stable production", "green"), ("Throughput", "82.4%", "+3.2% shift target", "cyan"), ("Safety systems", "12 / 12", "All armed", "green"), ("Response queue", "02", "Awaiting review", "amber")]):
    with col: metric_card(*args)

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>FACILITY STATE</div><h3>RigOS Alpha Refinery</h3><p class='muted'>All primary systems are operating within their configured envelope. AI supervision is active across five critical workflows.</p>" + status_chip("Running") + "</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<div class='section-label'>PROCESS ZONES</div>", unsafe_allow_html=True)
    st.dataframe([{"Zone": "Process A", "State": "Nominal", "Load": "78%", "Assets": 11}, {"Zone": "Process B", "State": "Monitoring", "Load": "86%", "Assets": 9}, {"Zone": "Terminal", "State": "Nominal", "Load": "69%", "Assets": 14}, {"Zone": "Utilities", "State": "Attention", "Load": "73%", "Assets": 8}], hide_index=True, use_container_width=True)
with right:
    st.markdown("<div class='section-label'>SUPERVISORY ACTIONS</div>", unsafe_allow_html=True)
    st.info("Controls are presentation-only in this demo. No operational commands are sent.")
    st.button("Acknowledge monitored alerts", use_container_width=True)
    st.button("Request AI situation brief", use_container_width=True)
    st.button("Open emergency response checklist", use_container_width=True)
    # TODO: Connect these controls to authenticated backend command/workflow endpoints.
```

## app/pages/4_Incident_Simulator.py

**File path:** `app/pages/4_Incident_Simulator.py`

```python

import sys
from pathlib import Path

import streamlit as st



ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from components.phase_one_views import render_incident_response_flow, render_live_signal_banner
from services.incident_service import IncidentService
from services.runtime import simulator
from ui_helpers import (
    incident_simulator_demo_flow,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip,
)
from components.incident_card import render_incident_card
from components.agent_card import render_agent_card
from components.telemetry_card import render_telemetry
from components.timeline import render_timeline
from components.investigation_progress import render_investigation_progress


setup_page("Incident Simulator")
render_sidebar("Incident Simulator")
page_heading(
    "SCENARIO LAB",
    "Incident Simulator",
    "Safely exercise AI detection, triage, and response workflows using synthetic events.",
)
render_live_signal_banner(
    "SCENARIO DESIGN MODE",
    "This interface visualizes the existing simulator flow and runs approved synthetic scenarios.",
    "Info",
)
st.write("")

left, right = st.columns([1, 1.35])
with left:
    st.markdown("<div class='section-label'>CONFIGURE SCENARIO</div>", unsafe_allow_html=True)
    asset = st.selectbox("Affected asset", ["Compressor C-12", "Pump A-01", "Valve V-09", "Heat Exchanger H-03"])
    incident_type = st.selectbox("Incident type", ["Pressure spike", "High temperature", "Gas leak", "High vibration", "Flow restriction"])
    severity = st.select_slider("Severity", options=["Low", "Medium", "High", "Critical"], value="High")
    automated = st.toggle("Enable AI workflow", value=True)
    launched = st.button("Launch simulated incident", use_container_width=True)
with right:
    render_incident_response_flow(incident_simulator_demo_flow(incident_type, asset))

if launched:
    st.success(f"Simulation launched for {asset}")
    service = IncidentService(simulator)
    simulator_result = service.trigger_incident(incident_type)
    render_incident_card(
        asset,
        incident_type,
        severity,
        "AI Investigation Complete" if simulator_result["reports"] else "Processing"
    )

    render_telemetry()
    render_timeline()
    render_investigation_progress()

    reports = simulator_result["reports"]

    if reports:
        for report in reports:
            render_agent_card(report)
    else:
        st.warning("No incident generated.")

    st.markdown("### ✅ System Recommendation")

    st.info(
        """
### Recommended Operator Actions

- Reduce pump speed by **20%**
- Verify discharge valve position
- Inspect the pressure relief valve
- Monitor pressure for **5 minutes**
- Do not restart until pressure remains below **135 PSI**
"""
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("✅ Approve Response Plan"):
            st.success("Response approved.")

    with c2:
        if st.button("🔄 Run Investigation Again"):
            st.info("Investigation restarted.")

    with c3:
        if st.button("📄 Generate Incident Report"):
            st.success("Report generation coming soon.")



st.write("")
st.markdown(
    "<div class='section-label'>RECENT SIMULATED SCENARIOS</div>",
    unsafe_allow_html=True,
)

st.dataframe(
    [
        {
            "Scenario": "SIM-772",
            "Type": "Gas leak",
            "Asset": "Tank T-04",
            "Result": "Resolved",
            "Duration": "3m 14s",
        },
        {
            "Scenario": "SIM-771",
            "Type": "High vibration",
            "Asset": "Compressor C-12",
            "Result": "Review required",
            "Duration": "2m 47s",
        },
    ],
    hide_index=True,
    use_container_width=True,
)

```

## app/pages/5_Knowledge_Base.py

**File path:** `app/pages/5_Knowledge_Base.py`

```python
import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page

setup_page("Knowledge Base")
render_sidebar("Knowledge Base")
page_heading("RETRIEVAL INTELLIGENCE", "Knowledge Base", "Search operational procedures, safety manuals, and maintenance guidance.")

query = st.text_input("Search approved operational knowledge", placeholder="e.g. pressure spike response procedure")
filters = st.columns(3)
with filters[0]: st.selectbox("Source", ["All sources", "SOP", "Safety manual", "Maintenance manual"])
with filters[1]: st.selectbox("Asset family", ["All assets", "Pumps", "Pipelines", "Tanks", "Compressors"])
with filters[2]: st.selectbox("Confidence", ["Any confidence", "90%+", "75%+"])

if query:
    st.success(f"Showing simulated results for “{query}”.")
    # TODO: Query the RAG retriever/knowledge agent through a stable backend API.

results = [
    ("Pressure SOP • Section 3.2", "Immediate stabilization actions for sustained discharge-pressure deviations.", "94% match"),
    ("Refinery Safety Handbook • Chapter 7", "Isolation, permit, and escalation requirements for abnormal process conditions.", "88% match"),
    ("Pump Maintenance Manual • Inspection", "Bearing, suction, and vibration checks for centrifugal pumping equipment.", "81% match"),
]
for title, summary, confidence in results:
    st.markdown(f"<div class='panel'><b>{title}</b><p class='muted'>{summary}</p><span style='color:#55d6ff;font-weight:700'>{confidence}</span></div>", unsafe_allow_html=True)
    st.write("")

st.markdown("<div class='section-label'>SUGGESTED SEARCHES</div>", unsafe_allow_html=True)
st.caption("Gas leak isolation • Compressor vibration limits • Flow restriction recovery • Emergency shutdown sequence")
```

## app/pages/6_Agent_Monitor.py

**File path:** `app/pages/6_Agent_Monitor.py`

```python
import streamlit as st
from components.phase_one_views import render_agent_execution_view, render_live_signal_banner
from ui_helpers import agent_monitor_demo_agents, metric_card, page_heading, render_sidebar, setup_page, status_chip

setup_page("Agent Monitor")
render_sidebar("Agent Monitor")
page_heading("AI SUPERVISION", "Agent Monitor", "Observe autonomous specialists, workflow handoffs, and decision confidence.")
render_live_signal_banner("DEMO AGENT STATE", "The current view preserves the existing demonstration data. Live registry and workflow state are pending backend integration.", "Info")
st.write("")

for col, args in zip(st.columns(4), [("Agents online", "5 / 5", "All systems available", "green"), ("Workflows active", "02", "1 awaiting input", "amber"), ("Avg. confidence", "94.6%", "+1.8% today", "cyan"), ("Decisions today", "128", "Within review SLA", "violet")]):
    with col: metric_card(*args)

st.write("")
agents = agent_monitor_demo_agents()
st.markdown("<div class='section-label'>AGENT FLEET</div>", unsafe_allow_html=True)
st.dataframe(agents, hide_index=True, use_container_width=True)

render_agent_execution_view(agents)

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>WORKFLOW PROGRESS</div>", unsafe_allow_html=True)
    st.progress(72, text="Vibration response workflow • 72% complete")
    st.progress(38, text="Pressure variance workflow • 38% complete")
with right:
    st.markdown("<div class='section-label'>LATEST HANDOFF</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'>{status_chip('Info')}<p><b>Diagnostic → Planning</b></p><span class='muted'>Root-cause confidence reached threshold. Recovery plan generation has been queued.</span></div>", unsafe_allow_html=True)
    # TODO: Surface live MAOKernel registry, scheduler, task, and report state
    # through an approved read-only backend integration; do not instantiate a kernel here.
```

## app/pages/7_Reports.py

**File path:** `app/pages/7_Reports.py`

```python
import streamlit as st
from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_report_detail_panel
from ui_helpers import metric_card, page_heading, render_sidebar, reports_demo_snapshot, setup_page

setup_page("Reports")
render_sidebar("Reports & Intelligence")
page_heading("DECISION RECORD", "Reports & Intelligence", "Review operational reports, AI recommendations, and response outcomes.")
render_live_signal_banner("REPORT DEMO REGISTER", "Existing demonstration records are shown until MAO execution reports are available through a read-only integration.", "Info")
st.write("")
snapshot = reports_demo_snapshot()

for col, args in zip(st.columns(4), snapshot["metrics"]):
    with col: metric_card(*args)

st.write("")
filters = st.columns(3)
with filters[0]: st.selectbox("Report type", ["All reports", "Incident response", "Asset health", "Maintenance", "Compliance"])
with filters[1]: st.selectbox("Status", ["All status", "Completed", "Pending review", "Escalated"])
with filters[2]: st.date_input("From date")

# TODO: Replace reports_demo_snapshot with execution reports exposed by MAO StateManager.
st.dataframe(snapshot["reports"], hide_index=True, use_container_width=True, height=240)

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>REPORT DETAIL PREVIEW</div>", unsafe_allow_html=True)
    render_report_detail_panel(snapshot["preview"])
with right:
    st.markdown("<div class='section-label'>EXPORT</div>", unsafe_allow_html=True)
    st.button("Prepare PDF briefing", use_container_width=True)
    st.button("Export report register", use_container_width=True)
    st.caption("Export controls are UI placeholders in this demo.")
```

## app/pages/8_Settings.py

**File path:** `app/pages/8_Settings.py`

```python
import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page

setup_page("Settings")
render_sidebar("Settings")
page_heading("WORKSPACE CONFIGURATION", "Settings", "Configure how Command Nexus presents information and routes operational notifications.")

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>DISPLAY & WORKSPACE</div>", unsafe_allow_html=True)
    st.selectbox("Default facility", ["RigOS Alpha Refinery", "North Terminal", "Training Sandbox"])
    st.selectbox("Default dashboard range", ["Last 24 hours", "Current shift", "Last 7 days"])
    st.toggle("Compact data tables", value=False)
    st.toggle("Show simulated-data badge", value=True)
with right:
    st.markdown("<div class='section-label'>NOTIFICATIONS</div>", unsafe_allow_html=True)
    st.toggle("Critical incident alerts", value=True)
    st.toggle("Daily operational digest", value=True)
    st.toggle("Agent workflow-completion alerts", value=False)
    st.selectbox("Escalation policy", ["Standard operational", "High sensitivity", "Training mode"])

st.write("")
left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>AI CONFIGURATION</div>", unsafe_allow_html=True)
    st.selectbox("Response profile", ["Balanced", "Safety-first", "Speed-first"])
    st.slider("Recommendation confidence threshold", 50, 100, 85, 5)
with right:
    st.markdown("<div class='section-label'>INTEGRATION STATUS</div>", unsafe_allow_html=True)
    st.dataframe([{"Integration": "Telemetry service", "State": "Demo mode"}, {"Integration": "MAO kernel", "State": "Not connected"}, {"Integration": "Knowledge retrieval", "State": "Not connected"}, {"Integration": "Notifications", "State": "Not connected"}], hide_index=True, use_container_width=True)

st.info("Changes are retained only for the current Streamlit session in this UI prototype.")
st.button("Save workspace preferences")
# TODO: Persist preferences and integration secrets through authenticated backend settings endpoints.
```

## app/pages/9_AI_Assistant.py

**File path:** `app/pages/9_AI_Assistant.py`

```python
import streamlit as st

from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_copilot_context_panel
from ui_helpers import append_copilot_backend_exchange, copilot_messages, page_heading, render_sidebar, setup_page


setup_page("AI Assistant")
render_sidebar("AI Operations Assistant")
page_heading("COPILOT", "AI Operations Assistant", "Ask for a concise operational brief, asset context, or safety-focused recommendation.")
render_live_signal_banner("COMMAND NEXUS ONLINE", "Your industrial operations copilot is ready for operational questions and shift support.", "Info")
st.write("")
messages = copilot_messages()

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>CONVERSATION</div>", unsafe_allow_html=True)
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
with right:
    render_copilot_context_panel()

prompt = st.chat_input("Ask Command Nexus...")
if prompt:
    with st.spinner("Command Nexus is preparing your response..."):
        append_copilot_backend_exchange(prompt)
    st.rerun()

# TODO: Route chat through an approved MAO chat/workflow endpoint when exposed.
# Never send Gemini keys to Streamlit or create a second MAOKernel here.
```

## app/ui_helpers.py

**File path:** `app/ui_helpers.py`

```python
"""Shared presentation and placeholder-data utilities for the Streamlit UI.

This module deliberately has no backend imports so each page remains runnable while
the Operations Center integration layer is being designed.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from random import Random

import streamlit as st

# Streamlit launched with ``streamlit run app/Home.py`` puts ``app/`` on
# sys.path. Use a frontend-specific package name to avoid shadowing the
# repository's backend ``services`` package.
from frontend_services.knowledge_agent_adapter import KnowledgeAgentUnavailable, ask_knowledge_agent


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
        .agent-card {

            padding:18px;
            border-radius:14px;
            background:rgba(255,255,255,0.05);
            border:1px solid rgba(255,255,255,0.15);
            margin-bottom:15px;

        }
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
    messages = copilot_messages()
    with st.sidebar.expander("✦ AI COPILOT", expanded=False):
        st.caption("Industrial operations copilot")
        for message in messages[-3:]:
            marker = "You" if message["role"] == "user" else "Nexus"
            st.caption(f"**{marker}:** {message['content']}")
        prompts = ["Summarize today's incidents", "Predict asset failures", "Explain system status", "Generate executive report", "Recommend maintenance"]
        prompt = st.selectbox("Suggested prompts", ["Select a prompt…"] + prompts, key="copilot_suggestion")
        typed = st.text_input("Ask Copilot", key="copilot_input", placeholder="Ask about operations")
        if st.button("Send", key="copilot_send", use_container_width=True):
            question = typed if typed.strip() else (prompt if prompt != "Select a prompt…" else "Explain system status")
            append_copilot_backend_exchange(question)
            st.rerun()
    # TODO: Replace direct agent invocation when the backend exposes an approved
    # MAO chat/workflow endpoint connected to the running orchestration process.


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


# Phase 1 frontend demo contracts. Replace these functions with a frontend
# service adapter once the backend team exposes an approved snapshot endpoint.
# TODO: Expected contract: system metrics, active incidents, assets, and recent
# agent activity from the *running* MAO/simulator process; never create a new kernel here.
def dashboard_demo_snapshot() -> dict:
    return {
        "metrics": [
            ("Fleet health", "88.4%", "+2.1% vs. prior shift", "green"),
            ("Assets online", "42 / 45", "3 under attention", "cyan"),
            ("Active incidents", "03", "1 requires escalation", "red"),
            ("AI decisions", "128", "94.6% confidence", "violet"),
        ],
        "assets": mock_assets(),
        "incidents": mock_incidents(),
        "activity": activity_items(),
    }


def incident_simulator_demo_flow(incident_type: str, asset: str) -> list[tuple[str, str]]:
    """Existing UI-only simulator flow; this function does not submit an event."""
    return [
        ("Detect", f"Synthetic {incident_type.lower()} signal selected for {asset}."),
        ("Triage", "Classify severity, assess the safety envelope, and create an incident record."),
        ("Orchestrate", "Route specialist agents through the matching response workflow."),
        ("Recommend", "Compile evidence, SOP guidance, and recovery actions for operator review."),
    ]


def agent_monitor_demo_agents() -> list[dict]:
    """Current agent-monitor display data, isolated for future MAO registry mapping."""
    return [
        {"Agent": "Safety", "Specialty": "Risk validation", "State": "Active", "Confidence": "96%", "Current task": "Check Compressor C-12"},
        {"Agent": "Diagnostic", "Specialty": "Root-cause analysis", "State": "Active", "Confidence": "95%", "Current task": "Analyze vibration pattern"},
        {"Agent": "Knowledge", "Specialty": "SOP retrieval", "State": "Ready", "Confidence": "93%", "Current task": "Awaiting request"},
        {"Agent": "Maintenance", "Specialty": "Maintenance planning", "State": "Ready", "Confidence": "94%", "Current task": "Awaiting task"},
        {"Agent": "Planning", "Specialty": "Recovery planning", "State": "Queued", "Confidence": "92%", "Current task": "Prepare recovery sequence"},
    ]


# TODO: Map agent_monitor_demo_agents to MAOKernel.registry, scheduler, and
# StateManager report/task data through an approved read-only backend interface.


# Phase 2 frontend demo contracts. These keep current demonstration content in
# one place while defining the data each page will require from a future adapter.
# TODO: Expected asset contract: asset identity/status/health and recent sensor
# telemetry from the running simulator/state manager, exposed read-only.
def asset_monitor_demo_snapshot() -> dict:
    return {
        "assets": mock_assets(),
        "sensors": [
            {"Sensor": "Pressure", "Reading": "119.4 bar", "State": "Normal"},
            {"Sensor": "Temperature", "Reading": "76.2 °C", "State": "Normal"},
            {"Sensor": "Vibration", "Reading": "23.7 mm/s", "State": "Watch"},
            {"Sensor": "Flow", "Reading": "63.1 m³/h", "State": "Normal"},
        ],
    }


# TODO: Expected report contract: execution report id/title/workflow/status,
# generated time, final summary, and recommendations from MAO StateManager.
def reports_demo_snapshot() -> dict:
    return {
        "metrics": [
            ("Reports generated", "128", "+18 today", "cyan"),
            ("Resolved incidents", "41", "92% within target", "green"),
            ("Average response", "4m 18s", "42 sec faster", "green"),
            ("Pending review", "06", "2 high priority", "amber"),
        ],
        "reports": [
            {"Report": "RPT-2048", "Title": "Compressor vibration response", "Workflow": "Maintenance response", "Status": "Pending review", "Generated": recent_dates(1)[0]},
            {"Report": "RPT-2047", "Title": "Valve pressure variance", "Workflow": "Pressure response", "Status": "Completed", "Generated": recent_dates(2)[0]},
            {"Report": "RPT-2046", "Title": "Heat exchanger excursion", "Workflow": "Temperature response", "Status": "Escalated", "Generated": recent_dates(3)[0]},
        ],
        "preview": {
            "Report": "RPT-2048",
            "Title": "Compressor vibration response",
            "Summary": "Diagnostic analysis indicates a likely bearing wear pattern. The recommended action is controlled load reduction followed by inspection within 24 hours.",
            "Recommendation": "Assign maintenance technician and verify suction pressure.",
        },
    }


def copilot_messages() -> list[dict]:
    """Return the persistent UI conversation, initialized with existing demo copy."""
    if "ops_messages" not in st.session_state:
        st.session_state.ops_messages = [{"role": "assistant", "content": "Command Nexus copilot online. Ask for an operational brief or recommendation."}]
    return st.session_state.ops_messages


def copilot_diagnostics() -> list[str]:
    """Return temporary frontend diagnostics for the current Copilot session."""
    if "copilot_diagnostics" not in st.session_state:
        st.session_state.copilot_diagnostics = []
    return st.session_state.copilot_diagnostics


def _record_copilot_diagnostic(message: str, callback=None) -> None:
    entry = f"{datetime.now().strftime('%H:%M:%S')} — {message}"
    diagnostics = copilot_diagnostics()
    diagnostics.append(entry)
    del diagnostics[:-25]
    if callback is not None:
        callback(entry)


def append_copilot_backend_exchange(question: str, diagnostic_callback=None) -> bool:
    """Append an existing KnowledgeAgent answer and retain its execution trace."""
    messages = copilot_messages()
    messages.append({"role": "user", "content": question})
    _record_copilot_diagnostic("Frontend received question; beginning backend request.", diagnostic_callback)
    try:
        answer = ask_knowledge_agent(
            question,
            on_progress=lambda stage: _record_copilot_diagnostic(stage, diagnostic_callback),
        )
    except Exception as error:
        _record_copilot_diagnostic(
            f"Frontend caught {type(error).__name__}: {error}",
            diagnostic_callback,
        )
        answer = "I’m unable to complete that request right now. Please try again shortly."
        messages.append({"role": "assistant", "content": answer})
        return False
    messages.append({"role": "assistant", "content": answer})
    _record_copilot_diagnostic("Assistant answer added to the conversation.", diagnostic_callback)
    return True


# TODO: Route copilot messages through an approved MAO chat/workflow endpoint
# once one exists; retain this thin adapter only until then.


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

    
```
