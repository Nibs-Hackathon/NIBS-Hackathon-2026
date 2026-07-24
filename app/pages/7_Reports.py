import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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

st.dataframe(snapshot["reports"], hide_index=True, use_container_width=True, height=240)

# Fix the render_report_detail_panel call
left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>REPORT DETAIL PREVIEW</div>", unsafe_allow_html=True)
    
    # ✅ Check if preview exists before rendering
    preview = snapshot.get("preview", {})
    if preview and preview.get("Report"):
        render_report_detail_panel(preview)
    else:
        st.info("Select a report to view details.")

import json
import pandas as pd
from datetime import datetime

# ... in the export section ...

with right:
    st.markdown("<div class='section-label'>EXPORT</div>", unsafe_allow_html=True)
    
    # ✅ PDF Briefing
    if st.button("📄 Prepare PDF briefing", use_container_width=True):
        from app.frontend_services.backend_api import api
        reports = api.get_reports()
        
        # Create a summary
        summary = f"""
        OPERATIONAL BRIEFING
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Total Reports: {len(reports)}
        Successful: {sum(1 for r in reports if r.get('success'))}
        Average Confidence: {sum(r.get('confidence', 0) for r in reports) / len(reports) * 100:.1f}%
        
        Recent Reports:
        """
        for r in reports[-3:]:
            summary += f"\n- {r.get('workflow')}: {r.get('summary', '')[:100]}..."
        
        st.download_button(
            label="📥 Download Briefing",
            data=summary,
            file_name=f"briefing_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    
    # ✅ Export Report Register
    if st.button("📊 Export report register", use_container_width=True):
        from app.frontend_services.backend_api import api
        reports = api.get_reports()
        
        # Create CSV
        df = pd.DataFrame(reports)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"reports_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )