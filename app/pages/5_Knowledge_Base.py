import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page

setup_page("Knowledge Base")
render_sidebar("Knowledge Base")
page_heading("RETRIEVAL INTELLIGENCE", "Knowledge Base", "Search operational procedures, safety manuals, and maintenance guidance.")

query = st.text_input("Search approved operational knowledge", placeholder="e.g. pressure spike response procedure")
filters = st.columns(3)
with filters[0]: st.selectbox("Source", ["All sources", "SOP", "Safety manual", "Maintenance manual"])
with filters[1]: st.selectbox("Asset family", ["All assets", "Pumps", "Pipelines", "Tanks", "Compressors"])
with filters[2]: st.selectbox("Confidence", ["Any confidence", "90%+", "75%+"])

if query:
    st.success(f"Showing simulated results for “{query}”.")
    # TODO: Query the RAG retriever/knowledge agent through a stable backend API.

results = [
    ("Pressure SOP • Section 3.2", "Immediate stabilization actions for sustained discharge-pressure deviations.", "94% match"),
    ("Refinery Safety Handbook • Chapter 7", "Isolation, permit, and escalation requirements for abnormal process conditions.", "88% match"),
    ("Pump Maintenance Manual • Inspection", "Bearing, suction, and vibration checks for centrifugal pumping equipment.", "81% match"),
]
for title, summary, confidence in results:
    st.markdown(f"<div class='panel'><b>{title}</b><p class='muted'>{summary}</p><span style='color:#55d6ff;font-weight:700'>{confidence}</span></div>", unsafe_allow_html=True)
    st.write("")

st.markdown("<div class='section-label'>SUGGESTED SEARCHES</div>", unsafe_allow_html=True)
st.caption("Gas leak isolation • Compressor vibration limits • Flow restriction recovery • Emergency shutdown sequence")
