"""Session-only presentation fallback for an empty local demo environment."""

from __future__ import annotations

import streamlit as st


def demo_mode_enabled() -> bool:
    """Return the operator's explicit, non-persistent demo-mode preference."""
    return bool(st.session_state.get("rigos_demo_mode", False))


def render_demo_mode_control() -> None:
    """Render one global opt-in control; no simulator or database writes occur."""
    st.checkbox(
        "Enable presentation Demo Mode",
        key="rigos_demo_mode",
        help="Shows labelled sample telemetry only when the live runtime has no data. It never writes to the simulator or database.",
    )


def sample_telemetry() -> list[dict]:
    """Return an explicitly synthetic, session-only telemetry sequence."""
    return [
        {"Sensor": "Vibration", "Observed": value, "Time": f"T-{index + 1}"}
        for index, value in enumerate((11.2, 11.8, 12.1, 12.7, 13.0, 13.4))
    ]
