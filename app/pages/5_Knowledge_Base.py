import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from components.global_notifications import render_global_notifications



# ✅ RENDER GLOBAL NOTIFICATIONS

import streamlit as st

from frontend_services.knowledge_adapter import KnowledgeSearchError, search_knowledge
from ui_helpers import page_heading, render_sidebar, setup_page


setup_page("Knowledge Base")
render_global_notifications()
render_sidebar("Knowledge Base")
page_heading(
    "RETRIEVAL INTELLIGENCE",
    "Knowledge Base",
    "Search the live operational procedures, safety manuals, and maintenance guidance in Neon.",
)

with st.form("knowledge_search", border=False):
    query = st.text_input(
        "Search approved operational knowledge",
        placeholder="e.g. pressure spike response procedure",
    )
    submitted = st.form_submit_button("Search knowledge", icon=":material/search:")

if submitted:
    if not query.strip():
        st.warning("Enter a search query to retrieve operational knowledge.")
    else:
        with st.spinner("Searching the operational knowledge base..."):
            try:
                st.session_state["knowledge_search_results"] = search_knowledge(query)
                st.session_state["knowledge_search_query"] = query.strip()
                st.session_state.pop("knowledge_search_error", None)
            except KnowledgeSearchError as error:
                st.session_state["knowledge_search_results"] = []
                st.session_state["knowledge_search_error"] = str(error)

if error := st.session_state.get("knowledge_search_error"):
    st.error(error)

results = st.session_state.get("knowledge_search_results")
if results is not None and not st.session_state.get("knowledge_search_error"):
    query_label = st.session_state.get("knowledge_search_query", "your query")
    if not results:
        st.info(f"No matching knowledge documents were found for “{query_label}”.")
    else:
        st.caption(f"{len(results)} live Neon retrieval result(s) for “{query_label}”")
        for index, result in enumerate(results, start=1):
            with st.expander(f"{index}. {result['filename']}", expanded=index == 1):
                st.caption(f"Source: {result['source']}")
                st.write(result["content"])