# Folder: backend/rag Code Inventory

Generated: 2026-07-25T06:14:25 UTC

Contains 16 project files.

## backend/rag/__init__.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/__init__.py`

```python

```

## backend/rag/chunker.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/chunker.py`

```python

```

## backend/rag/citation.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/citation.py`

```python

```

## backend/rag/embedder.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/embedder.py`

```python
"""Gemini Embedding Manager for RigOS."""

from __future__ import annotations

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ✅ Correct import
from services.llm import _has_invalid_gemini_proxy

logger = logging.getLogger(__name__)

load_dotenv()


class Embedder:
    """Singleton wrapper around Google's Gemini embedding model."""

    _model: Optional[GoogleGenerativeAIEmbeddings] = None

    # ✅ Fixed: Removed duplicates, supports up to 7 keys
    API_KEY_ENVIRONMENTS = (
        "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3",
        "GOOGLE_API_KEY_4", "GOOGLE_API_KEY_5", "GOOGLE_API_KEY_6",
        "GOOGLE_API_KEY_7",
        "GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3",
        "GEMINI_API_KEY_4", "GEMINI_API_KEY_5", "GEMINI_API_KEY_6",
        "GEMINI_API_KEY_7",
        "GOOGLE_API_KEY", "GEMINI_API_KEY",
    )

    def __init__(self):
        if Embedder._model is None:
            self._initialize()

    def _initialize(self) -> None:
        """Initialize Gemini embeddings once."""
        api_key = None
        selected_variable = None

        for variable in self.API_KEY_ENVIRONMENTS:
            value = os.getenv(variable)
            if value:
                api_key = value
                selected_variable = variable
                break

        if api_key is None:
            raise RuntimeError(
                "No Gemini API key found.\n\n"
                "Expected one of:\n"
                + "\n".join(f" - {v}" for v in self.API_KEY_ENVIRONMENTS)
            )

        logger.info("Initializing Gemini embeddings using %s", selected_variable)

        Embedder._model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key,
            client_args={"trust_env": False} if _has_invalid_gemini_proxy() else None,
        )

        logger.info("Gemini embeddings initialized successfully.")

    def get_model(self) -> GoogleGenerativeAIEmbeddings:
        """Return the embedding model."""
        if Embedder._model is None:
            self._initialize()
        return Embedder._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple documents."""
        return self.get_model().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query."""
        return self.get_model().embed_query(text)

    def __repr__(self) -> str:
        return "Embedder(model='models/gemini-embedding-001', dimensions=3072)"
```

## backend/rag/ingestion.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/ingestion.py`

```python
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
```

## backend/rag/knowledge.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/knowledge.py`

```python

```

## backend/rag/llm_manager.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/llm_manager.py`

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

__all__ = ["LLMManager"]
```

## backend/rag/llm.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/llm.py`

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

CloudLLM = LLMManager

__all__ = ["CloudLLM", "LLMManager"]
```

## backend/rag/loader.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/loader.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:


    def load(self, path):

        loader = PyPDFLoader(path)

        documents = loader.load()

        return documents
```

## backend/rag/neon_vector_store.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/neon_vector_store.py`

```python
from sqlalchemy import text
from langchain_core.documents import Document

from database.connection import get_session
from database.models import KnowledgeDB
from uuid import uuid4


class NeonVectorStore:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self._db = None

    def create(self, documents):
        """Create the vector store from a list of documents."""
        session = get_session()
        try:
            for doc in documents:
                vector = self.embeddings.embed_query(doc.page_content)
                row = KnowledgeDB(
                    id=str(uuid4()),
                    content=doc.page_content,
                    source=doc.metadata.get("source", "unknown"),
                    embedding=vector
                )
                session.add(row)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add_documents(self, documents):
        """Add documents to an existing vector store."""
        session = get_session()
        try:
            for doc in documents:
                vector = self.embeddings.embed_query(doc.page_content)
                row = KnowledgeDB(
                    id=str(uuid4()),
                    content=doc.page_content,
                    source=doc.metadata.get("source", "unknown"),
                    embedding=vector
                )
                session.add(row)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def clear(self):
        """Remove all indexed chunks."""
        session = get_session()
        try:
            deleted = session.query(KnowledgeDB).delete()
            session.commit()
            return deleted
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def count(self):
        """Return the number of searchable chunks."""
        session = get_session()
        try:
            return session.query(KnowledgeDB).count()
        finally:
            session.close()

    def similarity_search(self, query, k=5):
        """Search by query string."""
        session = get_session()
        try:
            vector = self.embeddings.embed_query(query)

            results = session.execute(
                text("""
                    SELECT content, source
                    FROM knowledge
                    ORDER BY embedding <-> :vector
                    LIMIT :limit
                """),
                {"vector": str(vector), "limit": k}
            )

            documents = []
            for row in results:
                documents.append(
                    Document(
                        page_content=row.content,
                        metadata={"source": row.source},
                    )
                )
            return documents
        finally:
            session.close()

    def similarity_search_by_vector(self, embedding, k=5):
        """Search by embedding vector."""
        session = get_session()
        try:
            results = session.execute(
                text("""
                    SELECT content, source
                    FROM knowledge
                    ORDER BY embedding <-> :vector
                    LIMIT :limit
                """),
                {"vector": str(embedding), "limit": k}
            )

            documents = []
            for row in results:
                documents.append(
                    Document(
                        page_content=row.content,
                        metadata={"source": row.source},
                    )
                )
            return documents
        finally:
            session.close()

    def get(self):
        """Return self for compatibility."""
        return self

    def as_retriever(self, search_kwargs=None):
        """Return a retriever interface."""
        from rag.retriever import Retriever
        return Retriever(self)
```

## backend/rag/parser.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/parser.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:

    def load(self, path):

        loader = PyPDFLoader(path)

        return loader.load()
```

## backend/rag/pipeline.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/pipeline.py`

```python
from rag.loader import DocumentLoader
from rag.splitter import DocumentSplitter
from rag.embedder import Embedder
from rag.vector_store import VectorStore


from pathlib import Path
from rag.loader import DocumentLoader
from rag.splitter import DocumentSplitter
from rag.embedder import Embedder
from rag.vector_store import VectorStore

# Default path for FAISS index
DEFAULT_INDEX_PATH = "./data/faiss_index"


class RAGPipeline:

    def build(self, pdfs, index_path=DEFAULT_INDEX_PATH):
        """Build a FAISS vector store from PDF files."""
        loader = DocumentLoader()
        splitter = DocumentSplitter()
        embedder = Embedder()

        docs = []
        for pdf in pdfs:
            docs.extend(loader.load(pdf))

        chunks = splitter.split(docs)
        
        # ✅ FIXED: Use create() instead of build()
        store = VectorStore(embedder)
        store.create(chunks)
        
        # ✅ FIXED: Pass path to save()
        store.save(index_path)

        return store
```

## backend/rag/reranker.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/reranker.py`

```python

```

## backend/rag/retriever.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/retriever.py`

```python
class Retriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store


    def retrieve(self, query):
        if hasattr(self.vector_store, "similarity_search"):
            return self.vector_store.similarity_search(query)

        db = self.vector_store.get()
        if db is None:
            return []
        return db.similarity_search(query)
```

## backend/rag/splitter.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/splitter.py`

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=800,

            chunk_overlap=150,

        )

    def split(self, docs):

        return self.splitter.split_documents(docs)
```

## backend/rag/vector_store.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/vector_store.py`

```python
import faiss

from langchain_community.vectorstores import FAISS


class VectorStore:


    def __init__(self, embeddings):

        self.embeddings = embeddings

        self.db = None



    def create(self, documents):

        self.db = FAISS.from_documents(

            documents,

            self.embeddings

        )



    def save(self, path):

        self.db.save_local(path)



    def load(self, path):

        self.db = FAISS.load_local(

            path,

            self.embeddings,

            allow_dangerous_deserialization=True

        )


    def get(self):

        return self.db
```
