# Folder: rag Code Inventory

Generated: 2026-07-23 12:30:25 UTC

Contains 15 project files.

## rag/__init__.py

**File path:** `rag/__init__.py`

```python

```

## rag/chunker.py

**File path:** `rag/chunker.py`

```python

```

## rag/citation.py

**File path:** `rag/citation.py`

```python

```

## rag/embedder.py

**File path:** `rag/embedder.py`

```python
"""
rag/embedder.py

Gemini Embedding Manager for RigOS

This module replaces the previous HuggingFace embedding model with
Google's Gemini embedding model (text-embedding-004).

The public API intentionally remains the same:

    embedder = Embedder()
    model = embedder.get_model()

so existing code such as VectorStore and Retriever continues to work.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

logger = logging.getLogger(__name__)

load_dotenv()


class Embedder:
    """
    Singleton wrapper around Google's Gemini embedding model.

    Compatible with:
        - FAISS
        - LangChain VectorStore
        - Retriever
        - Existing RigOS code

    Example
    -------
        embedder = Embedder()
        embeddings = embedder.get_model()
    """

    _model: Optional[GoogleGenerativeAIEmbeddings] = None

    API_KEY_ENVIRONMENTS = (
        "GOOGLE_API_KEY_1",
        "GOOGLE_API_KEY_2",
        "GOOGLE_API_KEY",
        "GEMINI_API_KEY_1",
        "GEMINI_API_KEY_2",
        "GEMINI_API_KEY",
    )

    def __init__(self):
        if Embedder._model is None:
            self._initialize()

    def _initialize(self) -> None:
        """
        Initialize Gemini embeddings once.
        """

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

        logger.info(
            "Initializing Gemini embeddings using %s",
            selected_variable,
        )

        Embedder._model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key,
        )

        logger.info("Gemini embeddings initialized successfully.")

    def get_model(self) -> GoogleGenerativeAIEmbeddings:
        """
        Returns the embedding model.

        This preserves compatibility with the previous implementation.

        Returns
        -------
        GoogleGenerativeAIEmbeddings
        """

        if Embedder._model is None:
            self._initialize()

        return Embedder._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple documents.
        """

        return self.get_model().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """
        Embed a single query.
        """

        return self.get_model().embed_query(text)

    def __repr__(self) -> str:
        return "Embedder(model='models/text-embedding-004')"
```

## rag/ingestion.py

**File path:** `rag/ingestion.py`

```python

```

## rag/knowledge.py

**File path:** `rag/knowledge.py`

```python

```

## rag/llm_manager.py

**File path:** `rag/llm_manager.py`

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

__all__ = ["LLMManager"]
```

## rag/llm.py

**File path:** `rag/llm.py`

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

CloudLLM = LLMManager

__all__ = ["CloudLLM", "LLMManager"]
```

## rag/loader.py

**File path:** `rag/loader.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:


    def load(self, path):

        loader = PyPDFLoader(path)

        documents = loader.load()

        return documents
```

## rag/parser.py

**File path:** `rag/parser.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:

    def load(self, path):

        loader = PyPDFLoader(path)

        return loader.load()
```

## rag/pipeline.py

**File path:** `rag/pipeline.py`

```python
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
```

## rag/reranker.py

**File path:** `rag/reranker.py`

```python

```

## rag/retriever.py

**File path:** `rag/retriever.py`

```python
class Retriever:


    def __init__(self, vector_store):

        self.db = vector_store



    def retrieve(self, query, k=3):

        results = self.db.similarity_search(

            query,

            k=k

        )

        return results
```

## rag/splitter.py

**File path:** `rag/splitter.py`

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

## rag/vector_store.py

**File path:** `rag/vector_store.py`

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
