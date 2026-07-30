"""Read-only knowledge access with an always-available local fallback."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class KnowledgeSearchError(RuntimeError):
    """Raised when no knowledge retrieval path is available."""


__all__ = ["KnowledgeSearchError", "list_knowledge_documents", "search_knowledge"]


def list_knowledge_documents() -> list[dict[str, object]]:
    """Return the local corpus catalog without requiring Neon or the simulator."""
    from rag.local_knowledge_store import LocalKnowledgeStore

    return LocalKnowledgeStore().catalog()


def search_knowledge(query: str) -> list[dict[str, str]]:
    """Search configured retrieval first, then the always-available local corpus."""
    normalized_query = query.strip()
    if not normalized_query:
        return []

    documents = []
    retrieval_source = "local_refinery_corpus"
    try:
        from services.runtime import runtime

        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is not None and agent.retriever is not None:
            documents = agent.retriever.retrieve(normalized_query)
            if documents:
                retrieval_source = "configured_hybrid_retriever"
    except Exception:
        # Runtime, Neon, or the agent may be unavailable during startup. Local
        # refinery references are intentionally independent of those services.
        documents = []

    if not documents:
        try:
            from rag.local_knowledge_store import LocalKnowledgeStore

            local_store = LocalKnowledgeStore()
            if local_store.count() == 0:
                raise KnowledgeSearchError("The local refinery knowledge corpus is empty.")
            documents = local_store.similarity_search(normalized_query, k=5)
        except KnowledgeSearchError:
            raise
        except Exception as error:
            raise KnowledgeSearchError(f"Local knowledge retrieval failed: {str(error)[:100]}") from error

    results = []
    for document in documents:
        metadata = document.metadata or {}
        source = str(metadata.get("source", "Unknown source"))
        results.append(
            {
                "content": document.page_content,
                "source": source,
                "filename": Path(source).name or source,
                "retrieval": retrieval_source,
            }
        )
    return results
