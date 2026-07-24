# Folder: app Code Inventory

Generated: 2026-07-24T03:28:50 UTC

Contains 38 project files.

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

## app/frontend_services/agent_activity_adapter.py

**File path:** `app/frontend_services/agent_activity_adapter.py`

```python
"""Activity view-model sourced from live MAO state and persisted audit events."""

from datetime import datetime
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import get_session
from database.repositories.activity_repo import ActivityRepository
from services.runtime import kernel


def _format_time(timestamp) -> str:
    return timestamp.strftime("%H:%M:%S") if timestamp else "Unknown"


def _runtime_activity() -> list[dict]:
    return [
        {
            "time": _format_time(getattr(result, "timestamp", None)),
            "agent": result.agent_name,
            "action": result.summary or result.finding or "No summary recorded.",
            "state": "Completed" if result.success else "Failed",
            "confidence": f"{round(result.confidence * 100)}%",
            "progress": 100,
            "timestamp": getattr(result, "timestamp", None),
        }
        for result in kernel.state.agent_results
    ]


def _persisted_activity() -> tuple[list[dict], str | None]:
    """Load immutable activity records without blocking live state rendering."""
    session = None
    try:
        session = get_session()
        events = ActivityRepository(session).get_recent()
        return [
            {
                "time": _format_time(event.created_at),
                "agent": event.source,
                "action": event.summary,
                "state": event.status.title(),
                "confidence": (
                    f"{round(event.confidence * 100)}%"
                    if event.confidence is not None
                    else "Not available"
                ),
                "progress": 100 if event.status.lower() == "completed" else 0,
                "timestamp": event.created_at,
            }
            for event in events
        ], None
    except Exception:
        return [], "Persisted activity is temporarily unavailable."
    finally:
        if session is not None:
            session.close()


def get_agent_activity() -> tuple[list[dict], str | None]:
    """Return the combined live MAO and persisted activity timeline."""
    runtime_events = _runtime_activity()
    persisted_events, warning = _persisted_activity()
    activity = runtime_events + persisted_events
    activity.sort(key=lambda event: event["timestamp"] or datetime.min, reverse=True)
    return activity, warning


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return summary metrics from current MAO agent results."""
    results = kernel.state.agent_results

    if not results:
        return [
            ("Activities today", "0", "Waiting for execution", "cyan"),
            ("Completed workflows", "0", "No executions", "green"),
            ("Human reviews", "0", "No pending review", "amber"),
            ("Avg confidence", "0%", "No data", "violet"),
        ]

    completed = sum(result.success for result in results)
    confidence = sum(result.confidence for result in results) / len(results)
    reviews = sum(result.requires_human_approval for result in results)

    return [
        ("Activities today", str(len(results)), "From MAO execution", "cyan"),
        ("Completed workflows", str(completed), "Successful executions", "green"),
        ("Human reviews", str(reviews), "Approval required", "amber"),
        ("Avg confidence", f"{round(confidence * 100, 1)}%", "Agent confidence", "violet"),
    ]
```

## app/frontend_services/agent_adapter.py

**File path:** `app/frontend_services/agent_adapter.py`

```python
"""Read-only view model for the agents registered on the shared MAO kernel."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel



def get_agents() -> list[dict[str, str]]:
    """Return registered agents and their latest execution state.

    ``AgentRegistry`` intentionally exposes ``all()`` rather than its private
    ``_agents`` dictionary.  Keeping that boundary here prevents the UI from
    breaking when the registry implementation changes.
    """
    agents = []
    for agent in kernel.registry.all():
        name = getattr(agent, "name", agent.__class__.__name__)
        result = get_latest_result(name)
        metadata = getattr(result, "metadata", {}) if result else {}
        agents.append(
            {
                "Agent": name.replace("_", " ").title(),
                "Specialty": agent.__class__.__name__.removesuffix("Agent"),
                "State": "Active" if result else "Ready",
                "Confidence": f"{round(result.confidence * 100)}%" if result else "N/A",
                "Current task": metadata.get("task_name", "Awaiting task"),
            }
        )
    return agents




def get_latest_result(agent_name: str):
    """Return the newest result for an agent, if the agent has run."""
    results = [
        result for result in kernel.state.agent_results
        if getattr(result, "agent_name", None) == agent_name
    ]
    return results[-1] if results else None


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return monitor metrics calculated from the live MAO state."""
    registered = kernel.registry.all()
    results = kernel.state.agent_results
    tasks = kernel.state.get_tasks()
    average_confidence = (
        sum(result.confidence for result in results) / len(results)
        if results else None
    )
    active_tasks = sum(
        str(getattr(task, "status", "")).upper().endswith("RUNNING")
        for task in tasks
    )
    return [
        ("Agents registered", str(len(registered)), "Shared MAO registry", "green"),
        ("Tasks active", str(active_tasks), f"{len(tasks)} task(s) tracked", "amber"),
        (
            "Avg. confidence",
            f"{round(average_confidence * 100, 1)}%" if average_confidence is not None else "N/A",
            "From completed agent results" if results else "No executions yet",
            "cyan",
        ),
        ("Decisions recorded", str(len(results)), "MAO agent executions", "violet"),
    ]
```

## app/frontend_services/asset_adapter.py

**File path:** `app/frontend_services/asset_adapter.py`

```python
from services.runtime import kernel


def get_assets():

    assets = kernel.asset_service.all_assets()

    return {
        "assets": [
            {
                "id": asset.id,
                "Asset": asset.name,
                "Type": asset.asset_type,
                "Zone": asset.location,
                "Health": asset.health,
                "Status": asset.status,
                "Last telemetry": "N/A",
            }
            for asset in assets
        ],
        "sensors": [],
        "history": []
    }
```

## app/frontend_services/control_adapter.py

**File path:** `app/frontend_services/control_adapter.py`

```python
"""Read-only facility state for the Control Center page.

The adapter deliberately reads the process-wide runtime kernel rather than
creating a page-local MAO kernel.
"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel


def get_control_state() -> dict:
    """Return a facility snapshot derived from live MAO runtime state."""
    assets = kernel.asset_service.all_assets()
    events = kernel.event_store.all()

    if not assets:
        return {
            "facility_mode": "NO ASSETS",
            "throughput": "N/A",
            "safety": "0 / 0",
            "queue": str(len(events)),
            "zones": [],
            "summary": "No assets are registered with the shared MAO runtime.",
        }

    healthy_assets = [
        asset for asset in assets if asset.status.lower() in {"running", "healthy"}
    ]
    average_health = sum(asset.health for asset in assets) / len(assets)
    facility_mode = "RUNNING" if healthy_assets else "ATTENTION"

    zones: dict[str, dict] = {}
    for asset in assets:
        zone = asset.location or "Unassigned"
        zones.setdefault(zone, {"assets": 0, "health": []})
        zones[zone]["assets"] += 1
        zones[zone]["health"].append(asset.health)

    zone_snapshot = []
    for name, data in sorted(zones.items()):
        average_zone_health = sum(data["health"]) / len(data["health"])
        zone_snapshot.append(
            {
                "Zone": name,
                "State": "Nominal" if average_zone_health >= 80 else "Attention",
                "Health": f"{round(average_zone_health)}%",
                "Assets": data["assets"],
            }
        )

    return {
        "facility_mode": facility_mode,
        "throughput": f"{round((len(healthy_assets) / len(assets)) * 100, 1)}%",
        "safety": f"{len(healthy_assets)} / {len(assets)}",
        "queue": str(len(events)),
        "zones": zone_snapshot,
        "summary": (
            f"{len(healthy_assets)} of {len(assets)} registered assets are operating "
            f"normally; average asset health is {round(average_health, 1)}%."
        ),
    }
```

## app/frontend_services/dashboard_adapter.py

**File path:** `app/frontend_services/dashboard_adapter.py`

```python
from services.runtime import kernel



def calculate_severity(event):

    payload = event.payload


    if "gas" in payload:
        return "Critical"


    if "pressure" in payload:

        return (
            "Critical"
            if payload["pressure"] > 160
            else "High"
        )


    if "temperature" in payload:

        return (
            "Critical"
            if payload["temperature"] > 100
            else "High"
        )


    if "vibration" in payload:

        return (
            "Critical"
            if payload["vibration"] > 40
            else "High"
        )


    if "flow" in payload:
        return "Medium"


    return "Unknown"



def get_dashboard():

    # -------------------------
    # Assets
    # -------------------------

    assets = kernel.asset_service.all_assets()

    asset_snapshot = []

    for asset in assets:

        asset_snapshot.append(
            {
                "Asset": asset.name,
                "Type": asset.asset_type,
                "Zone": asset.location,
                "Health": asset.health,
                "Status": asset.status,
            }
        )


    # -------------------------
    # Incidents
    # -------------------------

    incidents = []

    for event in kernel.event_store.all():

        incidents.append(
            {
                "Incident": event.name,

                "Asset": event.source,

                "Severity": calculate_severity(event),

                "Detected": event.timestamp.strftime(
                    "%H:%M:%S"
                )
            }
        )


    # -------------------------
    # Metrics
    # -------------------------

    metrics = [
        (
            "Fleet health",
            calculate_average_health(assets),
            "Calculated from assets",
            "green"
        ),

        (
            "Assets online",
            f"{len(assets)} / {len(assets)}",
            "Connected",
            "cyan"
        ),

        (
            "Active incidents",
            str(len(incidents)),
            "From EventStore",
            "red"
        ),

        (
            "AI decisions",
            str(len(kernel.state.agent_results)),
            "Agent executions",
            "violet"
        )
    ]


    # -------------------------
    # Activity
    # -------------------------

    activity = []

    for report in kernel.state.execution_reports[-5:]:

        activity.append(
            (
                str(report.completed_at),
                "MAO",
                report.final_summary
            )
        )


    return {
        "metrics": metrics,
        "incidents": incidents,
        "assets": asset_snapshot,
        "activity": activity,
    }



def calculate_average_health(assets):

    if not assets:
        return "0%"

    value = sum(
        asset.health
        for asset in assets
    ) / len(assets)

    return f"{round(value,1)}%"
```

## app/frontend_services/digital_twin_adapter.py

**File path:** `app/frontend_services/digital_twin_adapter.py`

```python
"""Read-only asset and telemetry view-model for the Digital Twin page."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel


def _reading_value(readings: list[Any], sensor_type: str) -> str:
    for reading in reversed(readings):
        reading_type = getattr(reading.sensor_type, "value", reading.sensor_type)
        if str(reading_type).lower() == sensor_type.lower():
            return f"{reading.value} {reading.unit}"
    return "Not available"


def _maintenance_recommendation(asset_id: str) -> str:
    for result in reversed(kernel.state.agent_results):
        if result.agent_name != "maintenance":
            continue
        if result.metadata.get("asset_id") != asset_id:
            continue
        recommendations = result.recommendations or result.evidence
        if recommendations:
            return recommendations[0]
    return "No maintenance recommendation is available for this asset."


def get_twin_assets() -> list[dict]:
    """Return current assets and latest observed telemetry from the runtime.

    Failure probability is intentionally unavailable because HealthService does
    not expose a prediction model yet.
    TODO: Populate failure probability from the future prediction service.
    """
    assets = []
    for asset in kernel.asset_service.all_assets():
        readings = kernel.state.get_history(asset.id)
        health = kernel.health.calculate_health(readings) if readings else asset.health
        assets.append(
            {
                "id": asset.id,
                "Asset": asset.name,
                "Category": getattr(asset.asset_type, "value", str(asset.asset_type)),
                "Zone": asset.location or "Unassigned",
                "Status": asset.status or ("Healthy" if health >= 80 else "Attention"),
                "Health": round(health, 1),
                "Temperature": _reading_value(readings, "temperature"),
                "Pressure": _reading_value(readings, "pressure"),
                "RPM": _reading_value(readings, "rpm"),
                "Failure": "Not available",
                "Recommendation": _maintenance_recommendation(asset.id),
            }
        )
    return assets
```

## app/frontend_services/health_adapter.py

**File path:** `app/frontend_services/health_adapter.py`

```python
from services.runtime import kernel


def get_asset_health(asset_id):

    readings = kernel.state.get_history(asset_id)

    health = kernel.health.calculate_health(
        readings
    )

    return {
        "health": health,
        "readings": readings
    }
```

## app/frontend_services/health_prediction_adapter.py

**File path:** `app/frontend_services/health_prediction_adapter.py`

```python
from services.runtime import kernel


def get_health_prediction(asset_id, horizon_days=14):

    readings = kernel.state.get_history(
        asset_id
    )


    current_health = kernel.health.calculate_health(
        readings
    )


    historical = calculate_history(
        readings
    )


    prediction = predict_degradation(
        current_health,
        horizon_days
    )


    failure_probability = calculate_failure_probability(
        current_health
    )


    return {

        "health": round(
            current_health
        ),

        "rul": calculate_rul(
            current_health
        ),

        "failure_probability": f"{failure_probability}%",

        "confidence": calculate_confidence(
            readings
        ),

        "historical": {
            "Historical health": historical
        },

        "predicted": {
            "Predicted health": prediction,
            "Intervention threshold":
                [70] * len(prediction)
        },

        "telemetry": format_telemetry(
            readings
        )
    }



def calculate_history(readings):

    history = []

    for i in range(len(readings)):

        health = kernel.health.calculate_health(
            readings[:i+1]
        )

        history.append(
            round(health,1)
        )

    return history



def predict_degradation(
    current,
    days
):

    prediction = []

    health = current


    for _ in range(days):

        health -= 0.5

        prediction.append(
            round(
                max(0, health),
                1
            )
        )

    return prediction



def calculate_failure_probability(
    health
):

    risk = 100 - health

    return min(
        100,
        round(risk)
    )



def calculate_rul(
    health
):

    if health > 90:
        return "90+ days"

    if health > 75:
        return "45 days"

    if health > 50:
        return "14 days"

    return "<7 days"



def calculate_confidence(
    readings
):

    if len(readings) > 20:
        return "90%"

    if len(readings) > 5:
        return "75%"

    return "Low"



def format_telemetry(readings):

    data = []

    for reading in readings[-10:]:

        data.append(
            {
                "Sensor": reading.sensor_type.value,

                "Observed": reading.value,

                "Time": reading.timestamp.strftime(
                    "%H:%M:%S"
                )
            }
        )

    return data
```

## app/frontend_services/incident_adapter.py

**File path:** `app/frontend_services/incident_adapter.py`

```python
from services.runtime import kernel, simulator
from services.incident_service import IncidentService


def trigger_incident(incident_type):

    service = IncidentService(
        simulator
    )

    return service.trigger_incident(
        incident_type
    )



def get_incidents():

    events = kernel.event_store.all()

    incidents = []

    for event in events:

        severity = calculate_severity(event)


        incidents.append(
            {
                "Incident": event.name,

                "Asset": event.source,

                "Severity": severity,

                "Detected": event.timestamp.strftime(
                    "%H:%M:%S"
                ),

                "Payload": event.payload,
            }
        )


    return incidents



def calculate_severity(event):

    payload = event.payload


    # derive severity from actual signal

    if "pressure" in payload:

        return (
            "Critical"
            if payload["pressure"] > 160
            else "High"
        )


    if "temperature" in payload:

        return (
            "Critical"
            if payload["temperature"] > 100
            else "High"
        )


    if "gas" in payload:

        return "Critical"


    if "vibration" in payload:

        return (
            "Critical"
            if payload["vibration"] > 40
            else "High"
        )


    if "flow" in payload:

        return "Medium"


    return "Unknown"
```

## app/frontend_services/knowledge_adapter.py

**File path:** `app/frontend_services/knowledge_adapter.py`

```python
"""Read-only Knowledge Base access through the shared MAO kernel."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

class KnowledgeSearchError(RuntimeError):
    """Raised when the registered knowledge retrieval path is unavailable."""


__all__ = ["KnowledgeSearchError", "search_knowledge"]


def search_knowledge(query: str) -> list[dict[str, str]]:
    """Return normalized Neon retrieval results from the registered KnowledgeAgent."""
    normalized_query = query.strip()
    if not normalized_query:
        return []

    try:
        # Delay backend initialization until the user submits a search.  This
        # keeps the page importable even while Neon/Gemini is unavailable.
        from services.runtime import kernel

        agent = kernel.registry.get("knowledge")
        if agent is None or agent.retriever is None:
            raise KnowledgeSearchError("The shared KnowledgeAgent is unavailable.")
    except KnowledgeSearchError:
        raise
    except Exception as error:
        raise KnowledgeSearchError("The shared KnowledgeAgent is unavailable.") from error

    try:
        documents = agent.retriever.retrieve(normalized_query)
    except Exception as error:
        raise KnowledgeSearchError("Knowledge retrieval could not be completed.") from error

    results = []
    for document in documents:
        metadata = document.metadata or {}
        source = str(metadata.get("source", "Unknown source"))
        results.append(
            {
                "content": document.page_content,
                "source": source,
                "filename": Path(source).name or source,
            }
        )
    return results
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
    "trip", "failure", "process", "telemetry", "sensor", "knowledge",
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
    """Return the KnowledgeAgent registered on the shared MAO kernel."""
    try:
        from services.runtime import kernel

        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise RuntimeError("KnowledgeAgent is not registered on the MAO kernel.")
        return agent
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

## app/frontend_services/maintenance_adapter.py

**File path:** `app/frontend_services/maintenance_adapter.py`

```python
"""Read-only maintenance planning data from the shared MAO runtime."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel


def _result_index() -> dict[tuple[str, str], Any]:
    """Index completed agent output by its workflow task and assigned agent."""
    return {
        (result.metadata.get("task_name", ""), result.agent_name): result
        for result in kernel.state.agent_results
    }


def _task_asset_name(task: Any, result: Any | None) -> str:
    """Resolve an asset label only when it is present in live task/result data."""
    input_data = getattr(task, "input_data", {}) or {}
    output_data = getattr(task, "output_data", {}) or {}
    for source in (input_data, output_data, getattr(result, "metadata", {}) or {}):
        asset_id = source.get("asset_name") or source.get("asset_id")
        if asset_id:
            asset = kernel.asset_service.get(asset_id)
            return asset.name if asset else str(asset_id)
    return "Not specified"


def _priority_label(priority: int) -> str:
    return f"P{max(1, min(int(priority), 3))}"


def get_maintenance_plan() -> dict:
    """Format state-manager tasks and agent output for the planner UI.

    TODO: Add a maintenance-task repository when schedule windows and crew
    assignments become persisted backend concepts.
    """
    results = _result_index()
    rows = []
    for task in kernel.state.get_tasks():
        result = results.get((task.name, task.assigned_agent))
        rows.append(
            {
                "Priority": _priority_label(task.priority),
                "Asset": _task_asset_name(task, result),
                "Work order": task.description,
                "Owner": task.assigned_agent.replace("_", " ").title(),
                "State": "Completed" if result and result.success else task.status.value.title(),
                "Confidence": (
                    f"{round(result.confidence * 100)}%" if result else "Not available"
                ),
            }
        )

    maintenance_results = [
        result for result in kernel.state.agent_results if result.agent_name == "maintenance"
    ]
    planning_results = [
        result for result in kernel.state.agent_results if result.agent_name == "planning"
    ]
    latest_maintenance = maintenance_results[-1] if maintenance_results else None
    latest_plan = planning_results[-1] if planning_results else None
    owners = defaultdict(int)
    for row in rows:
        owners[row["Owner"]] += 1

    rationale = []
    if latest_plan:
        rationale = latest_plan.recommendations or latest_plan.evidence
    elif latest_maintenance:
        rationale = latest_maintenance.recommendations or latest_maintenance.evidence

    return {
        "tasks": rows,
        "metrics": [
            ("Planned work", str(len(rows)), "From MAO task state", "cyan"),
            ("High priority", str(sum(row["Priority"] == "P1" for row in rows)), "P1 workflow tasks", "red"),
            ("Assigned teams", str(len(owners)), "Derived from task owners", "green"),
            ("Maintenance results", str(len(maintenance_results)), "Live MAO outputs", "violet"),
        ],
        "rationale": rationale,
        "priority": (
            latest_maintenance.metadata.get("priority", "Not available")
            if latest_maintenance
            else "Not available"
        ),
        "downtime": (
            latest_maintenance.metadata.get("downtime", "Not available")
            if latest_maintenance
            else "Not available"
        ),
    }
```

## app/frontend_services/report_adapter.py

**File path:** `app/frontend_services/report_adapter.py`

```python
from services.runtime import kernel


def get_reports():

    reports = kernel.state.execution_reports


    formatted_reports = []


    for report in reports:

        formatted_reports.append(
            {
                "Report": report.id[:8],

                "Title": report.workflow_name,

                "Workflow": report.workflow_name,

                "Status": (
                    "Completed"
                    if report.success
                    else "Escalated"
                ),

                "Generated": report.completed_at.strftime(
                    "%d %b %H:%M"
                ),
            }
        )


    preview = {}


    if reports:

        latest = reports[-1]


        preview = {
            "Report": latest.id[:8],

            "Title": latest.workflow_name,

            "Summary": latest.final_summary,

            "Recommendation": (
                "\n".join(
                    latest.recommendations
                )
                if latest.recommendations
                else "No recommendation generated."
            )
        }


    metrics = [

        (
            "Reports generated",
            str(len(reports)),
            "From MAO executions",
            "cyan"
        ),

        (
            "Resolved incidents",
            str(
                sum(
                    1
                    for r in reports
                    if r.success
                )
            ),
            "Successful workflows",
            "green"
        ),

        (
            "Average response",
            calculate_average_time(reports),
            "Execution duration",
            "green"
        ),

        (
            "Pending review",
            str(
                sum(
                    1
                    for r in reports
                    if not r.success
                )
            ),
            "Requires attention",
            "amber"
        )
    ]


    return {
        "metrics": metrics,
        "reports": formatted_reports,
        "preview": preview,
    }



def calculate_average_time(reports):

    if not reports:
        return "N/A"


    durations = []

    for report in reports:

        duration = (
            report.completed_at
            -
            report.started_at
        ).total_seconds()


        durations.append(duration)


    avg = sum(durations) / len(durations)


    return f"{round(avg,1)} sec"
```

## app/frontend_services/telemetry_adapter.py

**File path:** `app/frontend_services/telemetry_adapter.py`

```python
from services.runtime import kernel


def get_asset_telemetry(asset_id):

    readings = kernel.state.get_history(asset_id)

    history = []

    for reading in readings:
        history.append(
            {
                "Timestamp": reading.timestamp,
                "Sensor": reading.sensor_type,
                "Value": reading.value,
                "Unit": reading.unit,
            }
        )

    return {
        "history": history,
        "latest": history[-1] if history else None,
    }
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
from ui_helpers import (
    metric_card,
    page_heading,
    render_health_heatmap,
    render_sidebar,
    setup_page
)

from frontend_services.dashboard_adapter import get_dashboard

setup_page("Dashboard")
render_sidebar("Executive Dashboard")
page_heading("OVERVIEW", "Operations Dashboard", "Real-time operational intelligence across the facility.")
snapshot = get_dashboard()
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
    st.info(
        "Live health trend will appear after telemetry history is populated."
    )
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

from ui_helpers import (
    gauge_card,
    metric_card,
    page_heading,
    render_sidebar,
    setup_page
)

from frontend_services.asset_adapter import get_assets
from frontend_services.health_prediction_adapter import get_health_prediction


setup_page("Health Prediction")

render_sidebar("Predictive Health")


page_heading(
    "PREDICTIVE INTELLIGENCE",
    "Asset Health Prediction",
    "Forecast degradation risk early enough to plan safe, efficient intervention."
)



# -----------------------------
# Load assets
# -----------------------------

asset_snapshot = get_assets()

assets = asset_snapshot["assets"]


if not assets:
    st.warning("No assets available.")
    st.stop()


asset_names = [
    asset["Asset"]
    for asset in assets
]



# -----------------------------
# Asset selection
# -----------------------------

left, right = st.columns([1, 1.5])


with left:

    selected_name = st.selectbox(
        "Forecast asset",
        asset_names
    )


    horizon = st.select_slider(
        "Forecast horizon",
        options=[
            "7 days",
            "14 days",
            "30 days"
        ],
        value="14 days"
    )


    selected_asset = next(
        asset
        for asset in assets
        if asset["Asset"] == selected_name
    )


    horizon_days = int(
        horizon.split()[0]
    )


    profile = get_health_prediction(
        selected_asset["id"],
        horizon_days
    )


    st.markdown(
        """
        <div class='panel'>
        <div class='section-label'>
        MODEL STATUS
        </div>

        <b>Forecast engine: LIVE TELEMETRY MODE</b>

        <p class='muted'>
        Prediction generated from asset telemetry history
        and current health calculations.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )



# -----------------------------
# Prediction graph
# -----------------------------

with right:

    st.markdown(
        f"""
        <div class='section-label'>
        PROJECTED HEALTH · {selected_name.upper()}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.line_chart(
        profile["predicted"],
        height=280
    )



# -----------------------------
# Gauges
# -----------------------------

gauge_columns = st.columns(3)


with gauge_columns[0]:

    gauge_card(
        "Health score",
        profile["health"],
        "Current modeled condition",
        "#55D6FF"
    )


with gauge_columns[1]:

    confidence = profile["confidence"]

    if confidence.endswith("%"):
        confidence_value = int(
            confidence.replace("%","")
        )
    else:
        confidence_value = 50


    gauge_card(
        "Model confidence",
        confidence_value,
        "Evidence consistency",
        "#4FE3B2"
    )



with gauge_columns[2]:

    risk = profile["failure_probability"]

    risk_value = int(
        risk.replace("%","")
    )


    gauge_card(
        "Failure risk",
        risk_value,
        f"{horizon} probability",
        "#FF718D"
    )



# -----------------------------
# Metrics
# -----------------------------

for col, args in zip(
    st.columns(4),
    [
        (
            "Current health",
            f"{profile['health']}%",
            "Calculated from telemetry",
            "amber"
        ),

        (
            "Remaining useful life",
            profile["rul"],
            "Estimate before intervention",
            "cyan"
        ),

        (
            "Failure probability",
            profile["failure_probability"],
            f"At end of {horizon}",
            "red"
        ),

        (
            "Model confidence",
            profile["confidence"],
            "Evidence quality",
            "green"
        )
    ]
):

    with col:
        metric_card(*args)



st.write("")



# -----------------------------
# Historical health
# -----------------------------

left, right = st.columns([1.25,1])


with left:

    st.markdown(
        "<div class='section-label'>HISTORICAL HEALTH TIMELINE</div>",
        unsafe_allow_html=True
    )


    st.line_chart(
        profile["historical"],
        height=210
    )



with right:

    st.markdown(
        """
        <div class='section-label'>
        AI DECISION EXPLANATION
        </div>

        <div class='panel'>

        <b>Why this prediction was made</b>

        <p class='muted'>
        Prediction generated from current telemetry behaviour,
        sensor deviations, and asset condition history.
        </p>


        <b>Recommended action</b>

        <p class='muted'>
        Review operating conditions and schedule inspection
        based on calculated risk level.
        </p>


        <b>Expected impact</b>

        <p class='muted'>
        Early intervention reduces probability of unexpected downtime.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )



# -----------------------------
# Telemetry table
# -----------------------------

st.markdown(
    "<div class='section-label'>SUPPORTING TELEMETRY</div>",
    unsafe_allow_html=True
)


st.dataframe(
    profile["telemetry"],
    hide_index=True,
    use_container_width=True
)
```

## app/pages/11_Maintenance_Planner.py

**File path:** `app/pages/11_Maintenance_Planner.py`

```python
import streamlit as st

from frontend_services.maintenance_adapter import get_maintenance_plan
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Maintenance Planner")
render_sidebar("Maintenance Planner")
page_heading(
    "WORK ORCHESTRATION",
    "Maintenance Planner",
    "Turn MAO task state and recommendations into an executable maintenance view.",
)

plan = get_maintenance_plan()
for col, args in zip(st.columns(4), plan["metrics"]):
    with col:
        metric_card(*args)

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>RECOMMENDED WORK PLAN</div>", unsafe_allow_html=True)
    if plan["tasks"]:
        st.dataframe(plan["tasks"], hide_index=True, height=250, width="stretch")
    else:
        st.info("No MAO maintenance tasks have been generated yet.")

with right:
    st.markdown("<div class='section-label'>PLANNING STATUS</div>", unsafe_allow_html=True)
    st.metric("Latest priority", plan["priority"])
    st.metric("Estimated downtime", plan["downtime"])
    st.caption("Read-only view of tasks generated by the shared MAO runtime.")

st.write("")
left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>MAINTENANCE TIMELINE</div>", unsafe_allow_html=True)
    if plan["tasks"]:
        for task in plan["tasks"]:
            tone = "Critical" if task["Priority"] == "P1" else "Info"
            st.markdown(
                f"<div class='timeline-row'><span class='muted'>{task['Priority']}</span>"
                f"<span class='timeline-dot'></span><div class='panel'><b>{task['Work order']}</b> "
                f"&nbsp; {status_chip(tone)}<br><span class='muted'>Asset: {task['Asset']} "
                f"Â· Owner: {task['Owner']} Â· State: {task['State']}</span></div></div>",
                unsafe_allow_html=True,
            )
    else:
        st.caption("The timeline will populate when a maintenance workflow creates tasks.")

with right:
    st.markdown("<div class='section-label'>AI SCHEDULING RATIONALE</div>", unsafe_allow_html=True)
    if plan["rationale"]:
        st.markdown(
            "<div class='panel'><b>Latest MAO recommendations</b><ul>"
            + "".join(f"<li>{item}</li>" for item in plan["rationale"])
            + "</ul></div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("No planning-agent recommendation is available yet.")
```

## app/pages/12_AI_Activity.py

**File path:** `app/pages/12_AI_Activity.py`

```python
import streamlit as st

from frontend_services.agent_activity_adapter import get_agent_activity, get_agent_metrics
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("AI Activity")
render_sidebar("AI Activity Timeline")
page_heading(
    "AUTONOMY AUDIT",
    "AI Agent Activity Timeline",
    "A chronological, reviewable record of AI observation, reasoning, and workflow handoffs.",
)

for col, args in zip(st.columns(4), get_agent_metrics()):
    with col:
        metric_card(*args)

st.write("")
filter_col, search_col = st.columns([1, 2])
with filter_col:
    agent_filter = st.selectbox(
        "Agent",
        ["All agents", "Safety", "Diagnostic", "Knowledge", "Maintenance", "Planning"],
    )
with search_col:
    search_term = st.text_input(
        "Search activity", placeholder="Filter by asset, workflow, or action"
    )

st.markdown("<div class='section-label'>LIVE EXECUTION FLOW</div>", unsafe_allow_html=True)
events, activity_warning = get_agent_activity()
if activity_warning:
    st.caption(activity_warning)

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

for event in visible_events:
    state_tone = (
        "Running"
        if event["state"] == "Running"
        else ("Pending" if event["state"] == "Queued" else "Info")
    )
    st.markdown(
        f"<div class='timeline-row'><span class='muted'>{event['time']}</span>"
        f"<span class='timeline-dot {'pulse' if event['state'] == 'Running' else ''}'></span>"
        f"<div class='panel'><b>{event['agent']}</b> &nbsp; {status_chip(state_tone)}"
        f"<br><span class='muted'>{event['action']} Â· Confidence {event['confidence']}"
        f"</span></div></div>",
        unsafe_allow_html=True,
    )
    st.progress(event["progress"], text=f"{event['progress']}% execution progress")
```

## app/pages/13_Digital_Twin.py

**File path:** `app/pages/13_Digital_Twin.py`

```python
import streamlit as st

from frontend_services.digital_twin_adapter import get_twin_assets
from ui_helpers import page_heading, render_sidebar, setup_page, status_chip


setup_page("Digital Twin")
render_sidebar("Digital Twin")
page_heading(
    "FACILITY TOPOLOGY",
    "Digital Twin View",
    "A live operational map of facility zones, asset condition, and observed process signals.",
)

assets = get_twin_assets()
if not assets:
    st.info("No assets are registered with the shared MAO runtime.")
    st.stop()

selected_name = st.selectbox("Inspect digital-twin asset", [asset["Asset"] for asset in assets])
selected = next(asset for asset in assets if asset["Asset"] == selected_name)

st.markdown("<div class='section-label'>INTERACTIVE FACILITY LAYERS</div>", unsafe_allow_html=True)
columns = st.columns(4)
for col, asset in zip(columns * 2, assets):
    with col:
        st.markdown(
            f"<div class='panel twin-tile'><div class='section-label'>{asset['Zone']} Â· {asset['Category']}</div>"
            f"<b>{asset['Asset']}</b><p style='margin:.7rem 0'>{status_chip(asset['Status'])}</p>"
            f"<p class='muted'>Health: {asset['Health']}%<br>Temp: {asset['Temperature']} "
            f"Â· Pressure: {asset['Pressure']}<br>RPM: {asset['RPM']} "
            f"Â· Failure: {asset['Failure']}</p></div>",
            unsafe_allow_html=True,
        )

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown("<div class='section-label'>PROCESS CONNECTIONS</div>", unsafe_allow_html=True)
    zones = " &nbsp; â†’ &nbsp; ".join(sorted({asset["Zone"] for asset in assets}))
    st.markdown(
        "<div class='panel' style='text-align:center; padding:2rem'><b>REGISTERED ZONES</b>"
        f"<br><br><span class='muted'>{zones}</span></div>",
        unsafe_allow_html=True,
    )

with right:
    st.markdown("<div class='section-label'>SELECTED ASSET DETAIL</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='panel'><b>{selected['Asset']}</b><p>{status_chip(selected['Status'])}</p>"
        f"<span class='muted'>Health: {selected['Health']}%<br>Temperature: {selected['Temperature']}"
        f"<br>Pressure: {selected['Pressure']}<br>RPM: {selected['RPM']}"
        f"<br>Failure probability: {selected['Failure']}</span><hr>"
        f"<b>Maintenance recommendation</b><p class='muted'>{selected['Recommendation']}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>TWIN CONTROLS</div>", unsafe_allow_html=True)
    st.selectbox("Overlay", ["Asset health", "Live telemetry", "Incident severity", "Maintenance schedule"])
    st.toggle("Show process connections", value=True)
    st.toggle("Highlight active incidents", value=True)
```

## app/pages/2_Assets.py

**File path:** `app/pages/2_Assets.py`

```python
import streamlit as st

from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_asset_detail_panel

from ui_helpers import (
    metric_card,
    page_heading,
    render_sidebar,
    setup_page,
)

from frontend_services.asset_adapter import get_assets
from frontend_services.telemetry_adapter import get_asset_telemetry
from frontend_services.health_adapter import get_asset_health


# -------------------------
# Setup
# -------------------------

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")

page_heading(
    "FLEET INTELLIGENCE",
    "Asset Monitoring",
    "Health, telemetry, and operational posture for every connected asset."
)


render_live_signal_banner(
    "LIVE ASSET TELEMETRY",
    "Connected to RigOS backend state manager.",
    "Info"
)

st.write("")


# -------------------------
# Load assets
# -------------------------

snapshot = get_assets()

assets = snapshot["assets"]


if not assets:
    st.warning("No assets available.")
    st.stop()


# -------------------------
# Filters
# -------------------------

filters = st.columns(3)


with filters[0]:

    zones = [
        "All zones"
    ] + list(
        set(
            asset["Zone"]
            for asset in assets
        )
    )

    zone = st.selectbox(
        "Zone",
        zones
    )


with filters[1]:

    statuses = [
        "All statuses"
    ] + list(
        set(
            asset["Status"]
            for asset in assets
        )
    )

    status = st.selectbox(
        "Status",
        statuses
    )


with filters[2]:

    selected = st.selectbox(
        "Focus asset",
        [
            asset["Asset"]
            for asset in assets
        ]
    )


# -------------------------
# Filtered assets
# -------------------------

visible = [
    asset
    for asset in assets
    if (
        zone == "All zones"
        or asset["Zone"] == zone
    )
    and (
        status == "All statuses"
        or asset["Status"] == status
    )
]


st.dataframe(
    visible,
    hide_index=True,
    use_container_width=True,
    height=260
)


# -------------------------
# Selected asset
# -------------------------

selected_asset = next(
    asset
    for asset in assets
    if asset["Asset"] == selected
)


asset_id = selected_asset["id"]


# -------------------------
# Backend data
# -------------------------

health_data = get_asset_health(
    asset_id
)

telemetry_data = get_asset_telemetry(
    asset_id
)


# -------------------------
# Metrics
# -------------------------

health = health_data["health"]

health_status = (
    "Healthy"
    if health >= 80
    else "Warning"
)


latest = telemetry_data["latest"]


sensor_count = (
    len(snapshot["sensors"])
    if "sensors" in snapshot
    else 0
)


last_update = (
    latest["Timestamp"]
    if latest
    else "No telemetry"
)


metrics = [
    (
        "Selected asset",
        selected,
        "Telemetry connected",
        "cyan"
    ),
    (
        "Current health",
        f"{health}%",
        health_status,
        "green"
    ),
    (
        "Sensor coverage",
        f"{sensor_count}",
        "channels reporting",
        "green"
    ),
    (
        "Last update",
        str(last_update),
        "Backend state",
        "green"
    )
]


for col, args in zip(
    st.columns(4),
    metrics
):

    with col:
        metric_card(*args)


# -------------------------
# Trend + Detail
# -------------------------

left, right = st.columns(
    [1.55, 1]
)


with left:

    st.markdown(
        "<div class='section-label'>HEALTH & SAFETY TREND</div>",
        unsafe_allow_html=True
    )


    history = telemetry_data["history"]


    if history:

        st.line_chart(
            history,
            height=260
        )

    else:

        st.info(
            "No telemetry history available yet."
        )


with right:

    render_asset_detail_panel(
        selected_asset,
        snapshot["sensors"]
    )
```

## app/pages/3_Control_Center.py

**File path:** `app/pages/3_Control_Center.py`

```python
import streamlit as st

from frontend_services.control_adapter import get_control_state
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Control Center")
render_sidebar("Control Center")
page_heading(
    "MISSION CONTROL",
    "Control Center",
    "A protected command surface for supervising facility-level operating state.",
)

state = get_control_state()
summary = state.get("summary", "Live facility summary is not available yet.")
metrics = [
    ("Facility mode", state["facility_mode"], "Live backend state", "green"),
    ("Asset availability", state["throughput"], "Calculated from assets", "cyan"),
    ("Safety systems", state["safety"], "Online assets", "green"),
    ("Response queue", state["queue"], "Active EventStore entries", "amber"),
]
for col, args in zip(st.columns(4), metrics):
    with col:
        metric_card(*args)

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown(
        "<div class='panel'><div class='section-label'>FACILITY STATE</div>"
        f"<h3>{state['facility_mode'].title()}</h3>"
        f"<p class='muted'>{summary}</p>"
        f"{status_chip(state['facility_mode'])}</div>",
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown("<div class='section-label'>PROCESS ZONES</div>", unsafe_allow_html=True)
    if state["zones"]:
        st.dataframe(state["zones"], hide_index=True, width="stretch")
    else:
        st.info("No zone data is available because no assets are registered.")

with right:
    st.markdown("<div class='section-label'>SUPERVISORY ACTIONS</div>", unsafe_allow_html=True)
    st.info(
        "Command actions are unavailable until an authenticated MAO command endpoint is registered."
    )
    st.button("Acknowledge monitored alerts", disabled=True, width="stretch")
    st.button("Request AI situation brief", disabled=True, width="stretch")
    st.button("Open emergency response checklist", disabled=True, width="stretch")
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
from frontend_services.incident_adapter import trigger_incident
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
    simulator_result = trigger_incident(
        incident_type
    )
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

from frontend_services.knowledge_adapter import KnowledgeSearchError, search_knowledge
from ui_helpers import page_heading, render_sidebar, setup_page


setup_page("Knowledge Base")
render_sidebar("Knowledge Base")
page_heading(
    "RETRIEVAL INTELLIGENCE",
    "Knowledge Base",
    "Search the live operational procedures, safety manuals, and maintenance guidance in Neon.",
)

with st.form("knowledge_search", border=False):
    query = st.text_input(
        "Search approved operational knowledge",
        placeholder="e.g. pressure spike response procedure",
    )
    submitted = st.form_submit_button("Search knowledge", icon=":material/search:")

if submitted:
    if not query.strip():
        st.warning("Enter a search query to retrieve operational knowledge.")
    else:
        with st.spinner("Searching the operational knowledge base..."):
            try:
                st.session_state["knowledge_search_results"] = search_knowledge(query)
                st.session_state["knowledge_search_query"] = query.strip()
                st.session_state.pop("knowledge_search_error", None)
            except KnowledgeSearchError as error:
                st.session_state["knowledge_search_results"] = []
                st.session_state["knowledge_search_error"] = str(error)

if error := st.session_state.get("knowledge_search_error"):
    st.error(error)

results = st.session_state.get("knowledge_search_results")
if results is not None and not st.session_state.get("knowledge_search_error"):
    query_label = st.session_state.get("knowledge_search_query", "your query")
    if not results:
        st.info(f"No matching knowledge documents were found for “{query_label}”.")
    else:
        st.caption(f"{len(results)} live Neon retrieval result(s) for “{query_label}”")
        for index, result in enumerate(results, start=1):
            with st.expander(f"{index}. {result['filename']}", expanded=index == 1):
                st.caption(f"Source: {result['source']}")
                st.write(result["content"])
```

## app/pages/6_Agent_Monitor.py

**File path:** `app/pages/6_Agent_Monitor.py`

```python
import streamlit as st
from components.phase_one_views import render_agent_execution_view, render_live_signal_banner
from ui_helpers import (
    metric_card,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip
)

from frontend_services.agent_adapter import get_agent_metrics, get_agents

setup_page("Agent Monitor")
render_sidebar("Agent Monitor")
page_heading("AI SUPERVISION", "Agent Monitor", "Observe autonomous specialists, workflow handoffs, and decision confidence.")
render_live_signal_banner("LIVE MAO REGISTRY", "Agent registration and completed execution state are read from the shared backend kernel.", "Info")
st.write("")

for col, args in zip(st.columns(4), get_agent_metrics()):
    with col: metric_card(*args)

st.write("")
agents = get_agents()
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
from ui_helpers import (
    metric_card,
    page_heading,
    render_sidebar,
    setup_page
)

from frontend_services.report_adapter import get_reports
setup_page("Reports")
render_sidebar("Reports & Intelligence")
page_heading("DECISION RECORD", "Reports & Intelligence", "Review operational reports, AI recommendations, and response outcomes.")
render_live_signal_banner("REPORT DEMO REGISTER", "Existing demonstration records are shown until MAO execution reports are available through a read-only integration.", "Info")
st.write("")
snapshot = get_reports()

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
