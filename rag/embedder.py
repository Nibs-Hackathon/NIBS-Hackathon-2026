"""Gemini embedding manager for RigOS retrieval workflows."""

from __future__ import annotations

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from services.llm import _has_invalid_gemini_proxy


logger = logging.getLogger(__name__)

load_dotenv()


class Embedder:
    """Singleton wrapper that preserves the existing embedding API."""

    _model: Optional[GoogleGenerativeAIEmbeddings] = None

    API_KEY_ENVIRONMENTS = (
        "GOOGLE_API_KEY_1",
        "GOOGLE_API_KEY_2",
        "GOOGLE_API_KEY",
        "GEMINI_API_KEY_1",
        "GEMINI_API_KEY_2",
        "GEMINI_API_KEY",
    )

    def __init__(self) -> None:
        if Embedder._model is None:
            self._initialize()

    def _initialize(self) -> None:
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
                "No Gemini API key found. Expected one of: "
                + ", ".join(self.API_KEY_ENVIRONMENTS)
            )

        # Preserve the current process environment. Only this Gemini embedding
        # client opts out of the known dead loopback proxy.
        client_args = {"trust_env": False} if _has_invalid_gemini_proxy() else None
        logger.info("Initializing Gemini embeddings using %s", selected_variable)
        Embedder._model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key,
            client_args=client_args,
            # The persisted FAISS index uses 384-dimensional vectors. Keeping
            # this dimension preserves its compatibility until re-indexing is
            # explicitly scheduled.
            output_dimensionality=384,
        )
        logger.info("Gemini embeddings initialized successfully.")

    def get_model(self) -> GoogleGenerativeAIEmbeddings:
        if Embedder._model is None:
            self._initialize()
        return Embedder._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.get_model().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.get_model().embed_query(text)

    def __repr__(self) -> str:
        return "Embedder(model='models/gemini-embedding-001', dimensions=384)"
