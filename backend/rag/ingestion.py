from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
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


        root = Path(folder)

        for file in root.rglob("*.pdf"):

            print(
                f"Loading: {file}"
            )

            loader = PyPDFLoader(
                str(file)
            )

            docs = loader.load()

            documents.extend(docs)



        for pattern in ("*.md", "*.txt"):
            for file in root.rglob(pattern):
                print(f"Loading: {file}")
                documents.append(Document(
                    page_content=file.read_text(encoding="utf-8"),
                    metadata={"source": str(file)},
                ))

        if not documents:

            raise RuntimeError(
                "No PDF, Markdown, or text documents found in the knowledge folder"
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
