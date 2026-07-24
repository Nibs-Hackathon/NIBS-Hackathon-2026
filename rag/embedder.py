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