from pathlib import Path

from agents.base import Agent
from mao.models.result import AgentResult

class KnowledgeAgent(Agent):

    name = "knowledge"


    def __init__(self):

        self.retriever = None

        self.llm = None


    def _initialize_services(self):
        """Load the RAG stack only when a knowledge task is executed."""
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

        print(
            "[knowledge] Retrieving SOP information..."
        )



    def execute(self, task, context=None):

        self._initialize_services()

        query = task.description


        documents = self.retriever.retrieve(query)


        source_labels = []
        context_parts = []
        for index, document in enumerate(documents, start=1):
            metadata = document.metadata or {}
            source = Path(str(metadata.get("source", "Knowledge base document"))).name
            page = metadata.get("page")
            label = f"[{index}] {source}" + (f", page {page + 1}" if isinstance(page, int) else "")
            source_labels.append(label)
            context_parts.append(f"{label}\n{document.page_content}")

        context = "\n\n".join(context_parts)


        prompt = f"""

You are Command Nexus, an experienced refinery operations engineer.

Answer the operator naturally and professionally using ONLY the retrieved
knowledge-base material below. Do not copy document text or present raw
extraction bullets. Do not invent operating limits, causes, actions, or
citations that are not supported by the sources.

For any safety-critical point, be precise and state when the retrieved
material does not provide enough information. Provide a concise operational
rationale based on the source evidence, but do not reveal hidden chain-of-thought.


Question:

{query}


Retrieved refinery knowledge:

{context}


Respond with Markdown using this structure where applicable:

## Operational assessment
A concise, operator-friendly answer.

## Recommended actions
- Prioritized, grounded actions.

## Safety considerations
- Safety-critical constraints or escalation needs.

## Operational rationale
A brief explanation tied to the retrieved evidence.

## Sources
- Cite every source-backed claim using the supplied labels, for example [1].

"""


        answer = self.llm.generate(prompt)



        return AgentResult(

            agent_name=self.name,

            success=True,

            confidence=0.95,

            summary=answer,

            recommendations=[

                "Follow retrieved SOP",

                "Verify operating limits"

            ],

            metadata={

                "documents_used": len(documents),
                "sources": source_labels,

            }

        )



    def reflect(self, result):

        print(
            "[knowledge] Completed knowledge retrieval."
        )
