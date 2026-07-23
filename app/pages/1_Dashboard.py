import streamlit as st

from frontend_services.dashboard_adapter import get_dashboard
from ui_helpers import metric_card, page_heading, render_health_heatmap, render_sidebar, setup_page, status_chip


setup_page("Dashboard")
render_sidebar("Executive Dashboard")
page_heading("OVERVIEW", "Operations Dashboard", "Current operating state from the shared MAO runtime.")
snapshot = get_dashboard()

if snapshot["is_empty"]:
    st.info("No operational activity has been recorded yet. Start the approved simulator or submit a workflow to populate this view.")

for col, args in zip(st.columns(4), snapshot["metrics"][:4]):
    with col:
        metric_card(*args)
for col, args in zip(st.columns(4), snapshot["metrics"][4:]):
    with col:
        metric_card(*args)

st.write("")
st.markdown("<div class='section-label'>FACILITY HEALTH BY ZONE</div>", unsafe_allow_html=True)
render_health_heatmap(snapshot["zones"])

left, right = st.columns([1.65, 1])
with left:
    st.markdown("<div class='section-label'>REGISTERED ASSET HEALTH</div>", unsafe_allow_html=True)
    if snapshot["telemetry"]:
        st.bar_chart(snapshot["telemetry"], x="Asset", y="Health", height=265)
    else:
        st.info("Asset-health visualization will appear once runtime assets are registered.")
with right:
    st.markdown("<div class='section-label'>ATTENTION QUEUE</div>", unsafe_allow_html=True)
    if snapshot["incidents"]:
        for item in snapshot["incidents"][:5]:
            st.markdown(
                f"<div class='panel'><b>{item['Incident']}</b> &nbsp; {status_chip(item['Severity'])}<br>"
                f"<span class='muted'>{item['Asset']} · {item['Detected']}</span></div>",
                unsafe_allow_html=True,
            )
    else:
        st.success("No open incidents are recorded in the EventStore.")

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>ASSET WATCHLIST</div>", unsafe_allow_html=True)
    if snapshot["assets"]:
        st.dataframe(snapshot["assets"], hide_index=True, height=245)
    else:
        st.info("No registered assets are available.")
with right:
    st.markdown("<div class='section-label'>RECENT WORKFLOW ACTIVITY</div>", unsafe_allow_html=True)
    if snapshot["activity"]:
        for item in snapshot["activity"]:
            st.markdown(
                f"**{item['time']} · {item['actor']}** {status_chip(item['status'])}  \n"
                f"<span class='muted'>{item['text']}</span>",
                unsafe_allow_html=True,
            )
    else:
        st.caption("No execution report has been created in this runtime session.")
