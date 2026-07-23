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
