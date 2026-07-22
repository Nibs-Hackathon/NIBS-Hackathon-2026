"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

CloudLLM = LLMManager

__all__ = ["CloudLLM", "LLMManager"]
