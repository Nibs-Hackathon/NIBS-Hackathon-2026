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


        context = "\n\n".join(

            doc.page_content

            for doc in documents

        )


        prompt = f"""

You are an expert oil and gas operations assistant.

Answer the question using ONLY the SOP information below.


Question:

{query}


SOP Information:

{context}


Give response:

Immediate Actions:
-

Possible Causes:
-

Maintenance:
-

Safety Notes:
-

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

                "documents_used": len(documents)

            }

        )



    def reflect(self, result):

        print(
            "[knowledge] Completed knowledge retrieval."
        )
