import streamlit as st
from ui_helpers import (
    page_heading,
    render_sidebar,
    setup_page
)

from frontend_services.knowledge_adapter import search_knowledge

setup_page("Knowledge Base")
render_sidebar("Knowledge Base")
page_heading("RETRIEVAL INTELLIGENCE", "Knowledge Base", "Search operational procedures, safety manuals, and maintenance guidance.")

query = st.text_input("Search approved operational knowledge", placeholder="e.g. pressure spike response procedure")
filters = st.columns(3)
with filters[0]: st.selectbox("Source", ["All sources", "SOP", "Safety manual", "Maintenance manual"])
with filters[1]: st.selectbox("Asset family", ["All assets", "Pumps", "Pipelines", "Tanks", "Compressors"])
with filters[2]: st.selectbox("Confidence", ["Any confidence", "90%+", "75%+"])

if query:

    st.success(
        f"Searching knowledge base for “{query}”"
    )

    results = search_knowledge(query)


    if not results:

        st.warning(
            "No matching knowledge documents found."
        )


    for result in results:

        st.markdown(
            f"""
            <div class='panel'>

            <b>{result["Title"]}</b>

            <p class='muted'>
            {result["Summary"]}
            </p>

            <span style='color:#55d6ff;font-weight:700'>
            {result["Confidence"]}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
st.markdown("<div class='section-label'>SUGGESTED SEARCHES</div>", unsafe_allow_html=True)
st.caption("Gas leak isolation • Compressor vibration limits • Flow restriction recovery • Emergency shutdown sequence")
