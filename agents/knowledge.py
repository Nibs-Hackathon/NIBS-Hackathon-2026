from agents.base import Agent

from mao.models.result import AgentResult

from rag.embedder import Embedder
from rag.vector_store import VectorStore
from rag.retriever import Retriever
from rag.llm import CloudLLM



class KnowledgeAgent(Agent):

    name = "knowledge"


    def __init__(self):

        embedder = Embedder()

        store = VectorStore(embedder.get_model())

        store.load("data/faiss_index")

        self.retriever = Retriever(store.db)

        self.llm = CloudLLM()



    def think(self, task):

        print(
            "[knowledge] Retrieving SOP information..."
        )



    def execute(self, task):

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