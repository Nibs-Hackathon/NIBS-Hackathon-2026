"""Knowledge agent shared by MAO workflows and Command Nexus."""

from __future__ import annotations

from pathlib import Path

from agents.base import Agent
from mao.models.result import AgentResult


class KnowledgeAgent(Agent):
    """Retrieve refinery guidance for workflows and create grounded chat answers."""

    name = "knowledge"

    def __init__(self, vector_store=None):
        super().__init__()
        self.retriever = None
        self.llm = None
        if vector_store is not None:
            from rag.retriever import Retriever
            self.retriever = Retriever(vector_store)

    def _initialize_services(self, require_llm: bool) -> None:
        """Lazily load the persisted retrieval index and, for chat, Gemini."""
        if self.retriever is None:
            from rag.embedder import Embedder
            from rag.retriever import Retriever
            from rag.vector_store import VectorStore

            embedder = Embedder()
            store = VectorStore(embedder.get_model())
            store.load("data/faiss_index")
            self.retriever = Retriever(store.db)

        if require_llm and self.llm is None:
            from services.llm import LLMManager
            self.llm = LLMManager()

    def think(self, task):
        print(f"[knowledge] Preparing guidance for '{task.name}'.")

    def execute(self, task, context=None) -> AgentResult:
        """Support MAO workflow context and direct Command Nexus requests."""
        workflow_execution = context is not None
        self._initialize_services(require_llm=not workflow_execution)

        findings = self._get_metadata(context, "diagnosis").get("diagnosis", [])
        query = " ".join(findings) if findings else task.description
        documents = self.retriever.retrieve(query)

        references, summaries, source_labels, context_parts = self._document_details(documents)
        execution_plan = self._get_metadata(context, "planning").get("execution_plan", [])
        recommendations = list(execution_plan)
        if summaries:
            recommendations.append("Review retrieved operating procedures before execution.")

        metadata = {
            "query": query,
            "references": references,
            "documents": summaries,
            "sources": source_labels,
        }
        self._store_metadata(context, metadata)

        if workflow_execution:
            return AgentResult(
                agent_name=self.name,
                success=True,
                finding=f"{len(documents)} knowledge document(s) retrieved.",
                confidence=0.94,
                evidence=references,
                recommendations=recommendations,
                required_action="Consult retrieved documentation",
                requires_human_approval=False,
                metadata=metadata,
                summary=f"Knowledge retrieval completed with {len(documents)} matching document(s).",
            )

        answer = self.llm.generate(self._chat_prompt(query, "\n\n".join(context_parts)))
        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.95,
            evidence=source_labels,
            recommendations=["Follow approved operating procedures", "Verify operating limits"],
            metadata={"documents_used": len(documents), "sources": source_labels},
            summary=answer,
        )

    @staticmethod
    def _document_details(documents):
        references, summaries, source_labels, context_parts = [], [], [], []
        for index, document in enumerate(documents, start=1):
            metadata = document.metadata or {}
            source = Path(str(metadata.get("source", "Operational reference"))).name
            page = metadata.get("page")
            label = f"[{index}] {source}" + (f", page {page + 1}" if isinstance(page, int) else "")
            references.append(str(metadata.get("source", "Unknown")))
            summaries.append(document.page_content[:300])
            source_labels.append(label)
            context_parts.append(f"{label}\n{document.page_content}")
        return references, summaries, source_labels, context_parts

    @staticmethod
    def _chat_prompt(query: str, reference_material: str) -> str:
        return f"""
You are Command Nexus, an experienced refinery operations engineer.

Deliver a confident, concise, professional operational response using ONLY the
technical reference material supplied below. Do not copy passages verbatim.
Do not invent operating limits, causes, actions, or citations that the material
does not support. Never mention implementation details such as retrieval,
documents, a knowledge base, databases, RAG, prompts, models, or internal
systems.

For safety-critical matters, be exact. If the supplied material does not
establish a fact, say that it is not established by the available operating
information. Give a brief operational rationale without revealing hidden
chain-of-thought.

Question:
{query}

Technical reference material:
{reference_material}

Respond in Markdown with every section below, using concise bullets where
appropriate. Do not rename the headings:

## Situation Assessment
## Immediate Actions
## Safety Considerations
## Possible Root Causes
## Recommended Maintenance
## Operational Impact
## References

Only cite source-backed operational statements in **References**, using the
supplied labels, for example [1].
"""

    @staticmethod
    def _get_metadata(context, key):
        if isinstance(context, dict):
            return context.get("metadata", {}).get(key, {})
        if not hasattr(context, "metadata"):
            return {}
        return context.metadata.get(key, {})

    @staticmethod
    def _store_metadata(context, metadata) -> None:
        if context is None:
            return
        if isinstance(context, dict):
            context.setdefault("metadata", {})["knowledge"] = metadata
            return
        if not hasattr(context, "metadata"):
            context.metadata = {}
        context.metadata["knowledge"] = metadata

    def reflect(self, result):
        print("[knowledge] Operational assessment completed.")
