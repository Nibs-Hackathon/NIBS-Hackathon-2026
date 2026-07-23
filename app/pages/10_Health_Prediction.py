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
