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
    # ✅ Add default values to prevent KeyError
    report_id = report.get('Report', 'N/A')
    title = report.get('Title', 'Untitled')
    summary = report.get('Summary', 'No summary available.')
    recommendation = report.get('Recommendation', 'No recommendation available.')
    
    st.markdown(
        f"<div class='panel'><b>{report_id} · {title}</b>"
        f"<p class='muted'>{summary}</p>"
        f"<p><b>Recommendation:</b> {recommendation}</p></div>",
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
