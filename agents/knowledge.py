"""
agents/knowledge.py

Production Knowledge Agent

Responsibilities
----------------
- Query the RAG knowledge base
- Retrieve relevant SOPs and manuals
- Provide contextual recommendations
- Publish knowledge metadata
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from rag.retriever import Retriever


class KnowledgeAgent(Agent):

    name = "knowledge"

    def __init__(self,vector_store):

        super().__init__()
        self.retriever = Retriever(vector_store)

    def execute(self, task, context):

        diagnosis = self._get_metadata(
            context,
            "diagnosis",
        )

        planning = self._get_metadata(
            context,
            "planning",
        )

        findings = diagnosis.get(
            "diagnosis",
            [],
        )

        execution_plan = planning.get(
            "execution_plan",
            [],
        )

        query = self._build_query(findings)

        documents = []

        try:
            documents = self.retriever.retrieve(query)

        except Exception:

            documents = []

        references = []
        summaries = []

        for doc in documents:

            references.append(
                doc.metadata.get(
                    "source",
                    "Unknown"
                )
            )

            summaries.append(
                doc.page_content[:300]
            )

        recommendations = list(execution_plan)

        if summaries:

            recommendations.append(
                "Review retrieved operating procedures before execution."
            )

        metadata = {
            "query": query,
            "references": references,
            "documents": summaries,
        }

        self._store_metadata(
            context,
            metadata,
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=(
                f"{len(documents)} knowledge document(s) retrieved."
            ),
            confidence=0.94,
            evidence=references,
            recommendations=recommendations,
            required_action="Consult retrieved documentation",
            requires_human_approval=False,
            metadata=metadata,
            summary=(
                f"Knowledge retrieval completed with "
                f"{len(documents)} matching document(s)."
            ),
        )

    def _build_query(self, findings):

        if not findings:
            return "general oil and gas operational procedures"

        return " ".join(findings)

    def _get_metadata(self, context, key):

        if isinstance(context, dict):
            return context.get(
                "metadata",
                {},
            ).get(key, {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get(key, {})

    def _store_metadata(
        self,
        context,
        metadata,
    ):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["knowledge"] = metadata

            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["knowledge"] = metadata