from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embedder import Embedder
from rag.neon_vector_store import NeonVectorStore



class KnowledgeIngestion:


    def __init__(self):

        embedder = Embedder()

        self.vector_store = NeonVectorStore(
            embedder.get_model()
        )



    def ingest_folder(self, folder):

        documents = []


        for file in Path(folder).rglob("*.pdf"):

            print(
                f"Loading: {file}"
            )

            loader = PyPDFLoader(
                str(file)
            )

            docs = loader.load()

            documents.extend(docs)



        if not documents:

            raise RuntimeError(
                "No PDF documents found in docs/"
            )



        splitter = RecursiveCharacterTextSplitter(

            chunk_size=800,

            chunk_overlap=100

        )


        chunks = splitter.split_documents(
            documents
        )


        print(
            f"Created {len(chunks)} chunks"
        )



        self.vector_store.create(
            chunks
        )


        print(
            "Stored embeddings in Neon pgvector"
        )


        return len(chunks)