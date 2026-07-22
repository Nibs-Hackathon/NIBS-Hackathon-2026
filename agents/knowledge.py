from pathlib import Path

from agents.base import Agent
from mao.models.result import AgentResult


class KnowledgeAgent(Agent):
    """Grounded refinery operations agent used for technical questions."""

    name = "knowledge"

    def __init__(self):
        self.retriever = None
        self.llm = None

    def _initialize_services(self):
        """Load the operational reference stack only when it is required."""
        if self.retriever is not None and self.llm is not None:
            return

        from rag.embedder import Embedder
        from rag.retriever import Retriever
        from rag.vector_store import VectorStore
        from services.llm import LLMManager

        embedder = Embedder()
        store = VectorStore(embedder.get_model())
        store.load("data/faiss_index")
        self.retriever = Retriever(store.db)
        self.llm = LLMManager()

    def think(self, task):
        print("[knowledge] Preparing an operational assessment...")

    def execute(self, task, context=None):
        self._initialize_services()
        query = task.description
        documents = self.retriever.retrieve(query)

        source_labels = []
        context_parts = []
        for index, document in enumerate(documents, start=1):
            metadata = document.metadata or {}
            source = Path(str(metadata.get("source", "Operational reference"))).name
            page = metadata.get("page")
            label = f"[{index}] {source}" + (f", page {page + 1}" if isinstance(page, int) else "")
            source_labels.append(label)
            context_parts.append(f"{label}\n{document.page_content}")

        reference_material = "\n\n".join(context_parts)
        prompt = f"""
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
        answer = self.llm.generate(prompt)

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.95,
            summary=answer,
            recommendations=["Follow approved operating procedures", "Verify operating limits"],
            metadata={"documents_used": len(documents), "sources": source_labels},
        )

    def reflect(self, result):
        print("[knowledge] Operational assessment completed.")
