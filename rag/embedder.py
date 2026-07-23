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