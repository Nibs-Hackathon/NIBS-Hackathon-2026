from rag.loader import DocumentLoader
from rag.splitter import DocumentSplitter
from rag.embedder import Embedder
from rag.vector_store import VectorStore


class RAGPipeline:

    def build(self, pdfs):

        loader = DocumentLoader()

        splitter = DocumentSplitter()

        embedder = Embedder()

        docs = []

        for pdf in pdfs:

            docs.extend(

                loader.load(pdf)

            )

        chunks = splitter.split(docs)

        store = VectorStore(embedder)

        store.build(chunks)

        store.save()

        return store