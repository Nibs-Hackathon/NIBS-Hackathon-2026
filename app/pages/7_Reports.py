import csv
from io import StringIO

import streamlit as st

from components.phase_two_views import render_report_detail_panel
from frontend_services.report_adapter import get_reports
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page


def _export_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


setup_page("Reports")
render_sidebar("Reports & Intelligence")
page_heading("DECISION RECORD", "Reports & Intelligence", "Execution reports, agent decisions, and export-ready operational evidence.")
snapshot = get_reports()

for col, args in zip(st.columns(4), snapshot["metrics"]):
    with col:
        metric_card(*args)

if snapshot["is_empty"]:
    st.info("No execution reports are available yet. Completed MAO workflows will appear here automatically.")
    st.stop()

filters = st.columns(2)
with filters[0]:
    status_filter = st.selectbox("Status", ["All status", "Completed", "Escalated"])
with filters[1]:
    workflow_filter = st.selectbox("Workflow", ["All workflows"] + sorted({row["Workflow"] for row in snapshot["reports"]}))

rows = [
    row
    for row in snapshot["reports"]
    if (status_filter == "All status" or row["Status"] == status_filter)
    and (workflow_filter == "All workflows" or row["Workflow"] == workflow_filter)
]

st.markdown("<div class='section-label'>EXECUTION REPORT REGISTER</div>", unsafe_allow_html=True)
st.dataframe(
    rows,
    hide_index=True,
    height=260,
    column_config={
        "Summary": st.column_config.TextColumn("Summary", width="large"),
        "Recommendations": st.column_config.TextColumn("Recommendations", width="large"),
    },
)

if not rows:
    st.caption("No reports match the selected filters.")
    st.stop()

selected_report = st.selectbox("Inspect report", rows, format_func=lambda row: f"{row['Report']} · {row['Title']}")
left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>REPORT DETAIL PREVIEW</div>", unsafe_allow_html=True)
    render_report_detail_panel(
        {
            "Report": selected_report["Report"],
            "Title": selected_report["Title"],
            "Summary": selected_report["Summary"],
            "Recommendation": selected_report["Recommendations"],
        }
    )
    st.markdown("<div class='section-label'>EXECUTION CONTEXT</div>", unsafe_allow_html=True)
    st.caption(
        f"Workflow: {selected_report['Workflow']} · Agents: {selected_report['Agents']} · "
        f"Confidence: {selected_report['Confidence']} · Duration: {selected_report['Duration']}"
    )
    st.markdown("<div class='section-label'>AGENT EXECUTION TIMELINE</div>", unsafe_allow_html=True)
    timeline = snapshot["timelines"].get(selected_report["Report"], [])
    if timeline:
        st.dataframe(timeline, hide_index=True, height=180)
    else:
        st.caption("No agent-level results were retained with this report.")
with right:
    st.markdown("<div class='section-label'>EXPORT</div>", unsafe_allow_html=True)
    st.download_button(
        "Download report register (CSV)",
        data=_export_csv(rows),
        file_name="rigos_execution_reports.csv",
        mime="text/csv",
        width="stretch",
    )
    st.caption("The register is formatted for hand-off to an external briefing or PDF process.")
