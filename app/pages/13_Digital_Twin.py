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
