from rag.local_knowledge_store import LocalKnowledgeStore
from api.adapters.knowledge_agent_adapter import is_operational_query


def test_local_refinery_corpus_is_populated():
    store = LocalKnowledgeStore()

    assert store.count() >= 20


def test_local_refinery_catalog_is_browsable():
    store = LocalKnowledgeStore()
    catalog = store.catalog()

    assert len(catalog) >= 8
    assert all(entry["title"] and entry["source"] for entry in catalog)
    assert any(entry["id"] == "08_facility_operating_context" for entry in catalog)


def test_local_refinery_corpus_retrieves_india_guidance():
    store = LocalKnowledgeStore()

    results = store.similarity_search("monsoon coastal corrosion Mumbai", k=3)

    assert results
    assert any(
        "India" in document.page_content or "monsoon" in document.page_content.casefold()
        for document in results
    )


def test_local_refinery_corpus_retrieves_equipment_guidance():
    store = LocalKnowledgeStore()

    results = store.similarity_search("pump vibration bearing maintenance", k=3)

    assert results
    assert any("Pumps" in document.page_content for document in results)


def test_dashboard_attention_prompt_uses_operational_path():
    assert is_operational_query("What needs my attention?") is True
    assert is_operational_query("Hello there") is False
