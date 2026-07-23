import streamlit as st
from ui_helpers import metric_card, page_heading, recent_dates, render_sidebar, setup_page

setup_page("Reports")
render_sidebar("Reports & Intelligence")
page_heading("DECISION RECORD", "Reports & Intelligence", "Review operational reports, AI recommendations, and response outcomes.")

for col, args in zip(st.columns(4), [("Reports generated", "128", "+18 today", "cyan"), ("Resolved incidents", "41", "92% within target", "green"), ("Average response", "4m 18s", "42 sec faster", "green"), ("Pending review", "06", "2 high priority", "amber")]):
    with col: metric_card(*args)

st.write("")
filters = st.columns(3)
with filters[0]: st.selectbox("Report type", ["All reports", "Incident response", "Asset health", "Maintenance", "Compliance"])
with filters[1]: st.selectbox("Status", ["All status", "Completed", "Pending review", "Escalated"])
with filters[2]: st.date_input("From date")

# TODO: Replace this presentation dataset with execution reports from the backend.
reports = [{"Report": "RPT-2048", "Title": "Compressor vibration response", "Workflow": "Maintenance response", "Status": "Pending review", "Generated": recent_dates(1)[0]}, {"Report": "RPT-2047", "Title": "Valve pressure variance", "Workflow": "Pressure response", "Status": "Completed", "Generated": recent_dates(2)[0]}, {"Report": "RPT-2046", "Title": "Heat exchanger excursion", "Workflow": "Temperature response", "Status": "Escalated", "Generated": recent_dates(3)[0]}]
st.dataframe(reports, hide_index=True, use_container_width=True, height=240)

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>REPORT DETAIL PREVIEW</div><div class='panel'><b>RPT-2048 · Compressor vibration response</b><p class='muted'>Diagnostic analysis indicates a likely bearing wear pattern. The recommended action is controlled load reduction followed by inspection within 24 hours.</p><p><b>Recommendation:</b> Assign maintenance technician and verify suction pressure.</p></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>EXPORT</div>", unsafe_allow_html=True)
    st.button("Prepare PDF briefing", use_container_width=True)
    st.button("Export report register", use_container_width=True)
    st.caption("Export controls are UI placeholders in this demo.")
