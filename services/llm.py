"""Centralized, failover-safe access to Gemini models."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


class LLMManager:
    """Route all LLM requests through configured Gemini keys with failover."""

    def __init__(self, model_name="gemini-2.5-flash", temperature=0.2):
        self.model_name = model_name
        self.temperature = temperature
        self.keys = self._load_keys()
        self.current_key_index = 0

        if not self.keys:
            raise RuntimeError(
                "No Gemini API keys are configured. Add GOOGLE_API_KEY_1 and "
                "GOOGLE_API_KEY_2 to the project-root .env file."
            )

    @staticmethod
    def _load_keys():
        """Read new names first while retaining legacy names during migration."""
        names = (
            "GOOGLE_API_KEY_1",
            "GOOGLE_API_KEY_2",
            "GEMINI_API_KEY_1",
            "GEMINI_API_KEY_2",
        )
        return list(dict.fromkeys(
            key for name in names if (key := os.getenv(name))
        ))

    def _create_model(self, key):
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            api_key=key,
            temperature=self.temperature,
        )

    def generate(self, prompt):
        """Generate a response, switching keys after each provider failure."""
        last_error = None

        for _ in range(len(self.keys)):
            key_number = self.current_key_index + 1
            key = self.keys[self.current_key_index]

            try:
                return self._create_model(key).invoke(prompt).content
            except Exception as error:
                last_error = error
                logger.warning(
                    "Gemini request failed for configured key %s; trying failover.",
                    key_number,
                    exc_info=True,
                )
                self.current_key_index = (
                    self.current_key_index + 1
                ) % len(self.keys)

        raise RuntimeError(
            "All configured Gemini API keys failed. Check quota, permissions, "
            "and network access."
        ) from last_error

