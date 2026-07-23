import streamlit as st

from frontend_services.asset_adapter import get_assets
from frontend_services.health_prediction_adapter import get_health_prediction
from ui_helpers import gauge_card, metric_card, page_heading, render_sidebar, setup_page


def _score(value: str | int | float | None) -> int:
    if value is None or value == "Not available":
        return 0
    return max(0, min(100, int(float(str(value).replace("%", "")))))


setup_page("Health Prediction")
render_sidebar("Predictive Health")
page_heading("PREDICTIVE INTELLIGENCE", "Asset Health Prediction", "Persisted PredictionAgent outputs with supporting runtime telemetry.")

assets = get_assets()["assets"]
if not assets:
    st.warning("No assets are available from the shared MAO runtime.")
    st.stop()

left, right = st.columns([1, 1.5])
with left:
    selected_name = st.selectbox("Forecast asset", [asset["Asset"] for asset in assets])
    horizon = st.select_slider("Requested forecast horizon", options=["7 days", "14 days", "30 days"], value="14 days")
    selected_asset = next(asset for asset in assets if asset["Asset"] == selected_name)
    profile = get_health_prediction(selected_asset["id"], int(horizon.split()[0]))
    if profile["is_demo"]:
        st.warning("Demo Mode: sample telemetry is shown locally because this asset has no live readings. Nothing is persisted.")
    if profile["warning"]:
        st.caption(profile["warning"])
    st.markdown("<div class='panel'><div class='section-label'>MODEL STATUS</div>", unsafe_allow_html=True)
    if profile["has_prediction"]:
        st.markdown("<b>Prediction source: PERSISTED PREDICTION AGENT OUTPUT</b>", unsafe_allow_html=True)
        st.caption("Forecast values are read from existing MAO prediction records.")
    else:
        st.markdown("<b>Prediction source: AWAITING PREDICTION AGENT OUTPUT</b>", unsafe_allow_html=True)
        st.caption("Current observed health is shown when available; no forecast is manufactured.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown(f"<div class='section-label'>PERSISTED PREDICTION HISTORY · {selected_name.upper()}</div>", unsafe_allow_html=True)
    if profile["predicted"]["Prediction health"]:
        st.line_chart(profile["predicted"], height=280)
    else:
        st.info("No persisted prediction is available for this asset yet.")

for col, args in zip(
    st.columns(3),
    [
        ("Health score", _score(profile["health"]), "Latest observed or predicted condition", "#55D6FF"),
        ("Model confidence", _score(profile["confidence"]), "Persisted prediction evidence", "#4FE3B2"),
        ("Failure risk", _score(profile["failure_probability"]), f"Requested horizon: {horizon}", "#FF718D"),
    ],
):
    with col:
        gauge_card(*args)

for col, args in zip(
    st.columns(4),
    [
        ("Current health", f"{profile['health']}%" if profile["health"] is not None else "Not available", "Observed runtime condition", "amber"),
        ("Remaining useful life", profile["rul"], "Persisted prediction value", "cyan"),
        ("Failure probability", profile["failure_probability"], "Persisted prediction value", "red"),
        ("Model confidence", profile["confidence"], "Persisted prediction evidence", "green"),
    ],
):
    with col:
        metric_card(*args)

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>OBSERVED HEALTH TIMELINE</div>", unsafe_allow_html=True)
    if profile["historical"]["Observed health"]:
        st.line_chart({"Observed health": profile["historical"]["Observed health"]}, height=210)
    else:
        st.caption("Observed health timeline will populate as telemetry arrives.")
with right:
    st.markdown("<div class='section-label'>AI DECISION EVIDENCE</div>", unsafe_allow_html=True)
    if profile["evidence"]:
        st.markdown("<div class='panel'><b>Prediction evidence</b><ul>" + "".join(f"<li>{item}</li>" for item in profile["evidence"]) + "</ul></div>", unsafe_allow_html=True)
    else:
        st.info("Evidence will appear with the next PredictionAgent result.")

st.markdown("<div class='section-label'>SUPPORTING TELEMETRY</div>", unsafe_allow_html=True)
if profile["telemetry"]:
    st.dataframe(profile["telemetry"], hide_index=True)
else:
    st.caption("No telemetry has been recorded for this asset.")
