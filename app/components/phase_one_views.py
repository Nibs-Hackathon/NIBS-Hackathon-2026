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
