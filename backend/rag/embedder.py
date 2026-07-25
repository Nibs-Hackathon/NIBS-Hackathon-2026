"""Quota-aware Gemini embeddings with the same key rotation policy as chat."""

from __future__ import annotations

import logging
import os
import re
import time
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from services.llm import MULTI_KEY_ENV_VARS, SUPPORTED_GEMINI_ENV_VARS, _has_invalid_gemini_proxy

logger = logging.getLogger(__name__)
load_dotenv()


class Embedder:
    """LangChain-compatible embedding proxy that rotates configured Gemini keys.

    ``get_model`` intentionally returns this proxy, rather than a provider
    object, so Neon and FAISS searches cannot bypass quota handling.
    """

    _keys: Optional[list[str]] = None
    _models: dict[str, GoogleGenerativeAIEmbeddings] = {}
    _cooldowns: dict[str, float] = {}
    _next_key_index = 0
    model_name = "models/gemini-embedding-001"

    def __init__(self):
        if Embedder._keys is None:
            Embedder._keys = self._load_keys()
        if not Embedder._keys:
            raise RuntimeError("No Gemini API key found for embeddings.")

    @staticmethod
    def _load_keys() -> list[str]:
        keys, seen = [], set()
        for variable in MULTI_KEY_ENV_VARS:
            for value in (os.getenv(variable) or "").split(","):
                value = value.strip()
                if value and value not in seen:
                    seen.add(value)
                    keys.append(value)
        for variable in SUPPORTED_GEMINI_ENV_VARS:
            value = os.getenv(variable)
            if value and value not in seen:
                seen.add(value)
                keys.append(value)
        logger.info("Embedding router initialized with %d Gemini key(s)", len(keys))
        return keys

    @staticmethod
    def _retry_delay_seconds(error: str) -> float:
        match = re.search(r"(?:retryDelay|retry in)[:\s]+['\"]?(\d+(?:\.\d+)?)s", error, re.IGNORECASE)
        return float(match.group(1)) + 1 if match else 60.0

    @classmethod
    def _next_available_key(cls) -> Optional[str]:
        keys = cls._keys or []
        now = time.time()
        for _ in range(len(keys)):
            key = keys[cls._next_key_index]
            cls._next_key_index = (cls._next_key_index + 1) % len(keys)
            if cls._cooldowns.get(key, 0) <= now:
                return key
        return None

    @classmethod
    def _model_for(cls, key: str) -> GoogleGenerativeAIEmbeddings:
        if key not in cls._models:
            cls._models[key] = GoogleGenerativeAIEmbeddings(
                model=cls.model_name,
                google_api_key=key,
                client_args={"trust_env": False} if _has_invalid_gemini_proxy() else None,
            )
        return cls._models[key]

    def _embed(self, operation: str, payload):
        last_error = None
        keys = Embedder._keys or []
        for _ in range(len(keys)):
            key = self._next_available_key()
            if key is None:
                break
            try:
                return getattr(self._model_for(key), operation)(payload)
            except Exception as error:
                last_error = error
                message = str(error)
                if "429" in message or "RESOURCE_EXHAUSTED" in message:
                    Embedder._cooldowns[key] = time.time() + self._retry_delay_seconds(message)
                    logger.warning("Embedding key quota reached; rotating to the next configured key.")
                    continue
                logger.warning("Embedding request failed; rotating to the next configured key.")
                Embedder._cooldowns[key] = time.time() + 10
        retry_after = min((until for until in Embedder._cooldowns.values() if until > time.time()), default=time.time() + 60)
        wait = max(1, round(retry_after - time.time()))
        raise RuntimeError(f"Embedding capacity is temporarily unavailable. Retry in about {wait} seconds.") from last_error

    def get_model(self):
        return self

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed("embed_documents", texts)

    def embed_query(self, text: str) -> list[float]:
        return self._embed("embed_query", text)

    def __repr__(self) -> str:
        return f"Embedder(model='{self.model_name}', rotating_keys={len(self._keys or [])})"
