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