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
