from rag.embedder import Embedder
from rag.vector_store import VectorStore
from rag.retriever import Retriever

embedder = Embedder()

store = VectorStore(embedder)
store.load()

retriever = Retriever(store.db)

results = retriever.retrieve(
    "How do I respond to a pressure spike?"
)

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content)