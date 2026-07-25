"""Read-only Knowledge Base access through the shared MAO kernel."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


class KnowledgeSearchError(RuntimeError):
    """Raised when the registered knowledge retrieval path is unavailable."""


__all__ = ["KnowledgeSearchError", "search_knowledge"]

def search_knowledge(query: str) -> list[dict[str, str]]:
    """Return normalized Neon retrieval results from the registered KnowledgeAgent."""
    normalized_query = query.strip()
    if not normalized_query:
        return []

    try:
        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise KnowledgeSearchError("Knowledge Agent is not available. Please ensure the knowledge base is loaded.")
        if agent.retriever is None:
            raise KnowledgeSearchError("Knowledge retriever is not initialized. Please build the knowledge base first.")
    except KnowledgeSearchError:
        raise
    except Exception as error:
        raise KnowledgeSearchError(f"Knowledge service unavailable: {str(error)[:100]}") from error

    try:
        documents = agent.retriever.retrieve(normalized_query)
    except Exception as error:
        raise KnowledgeSearchError(f"Retrieval failed: {str(error)[:100]}") from error

    results = []
    for document in documents:
        metadata = document.metadata or {}
        source = str(metadata.get("source", "Unknown source"))
        results.append(
            {
                "content": document.page_content,
                "source": source,
                "filename": Path(source).name or source,
            }
        )
    return results