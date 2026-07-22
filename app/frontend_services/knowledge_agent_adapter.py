"""Minimal frontend adapter for the existing RAG-backed KnowledgeAgent.

This adapter does not implement prompting, retrieval, or model access. It
constructs the existing MAO Task model and invokes KnowledgeAgent.execute(),
which continues to own FAISS retrieval and CloudLLM/Gemini generation.
"""

from __future__ import annotations

from functools import lru_cache
import logging
from pathlib import Path
import re
import sys
from typing import TYPE_CHECKING, Callable

# Streamlit running ``app/Home.py`` places ``app/`` on sys.path, but the
# existing backend packages (mao/, agents/, rag/, services/) live at the
# repository root. Resolve that root from this adapter's verified location:
# <repo>/app/frontend_services/knowledge_agent_adapter.py.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mao.models.task import Task

if TYPE_CHECKING:
    from agents.knowledge import KnowledgeAgent


LOGGER = logging.getLogger(__name__)
ProgressCallback = Callable[[str], None]

OPERATIONAL_KEYWORDS = (
    "asset",
    "compressor",
    "pump",
    "pipeline",
    "tank",
    "valve",
    "maintenance",
    "inspection",
    "incident",
    "alarm",
    "safety",
    "hazard",
    "pressure",
    "temperature",
    "vibration",
    "flow",
    "gas",
    "refinery",
    "sop",
    "procedure",
)


def conversational_response(question: str) -> str | None:
    """Handle lightweight conversational intents without initializing RAG.

    Operational language always takes precedence, so requests such as "help
    with pump maintenance" continue to use the existing KnowledgeAgent.
    """
    normalized = re.sub(r"\s+", " ", question.strip().casefold())
    if not normalized or any(keyword in normalized for keyword in OPERATIONAL_KEYWORDS):
        return None

    greeting_patterns = ("hi", "hello", "hey", "good morning", "good evening")
    if normalized in greeting_patterns or any(normalized.startswith(f"{greeting} ") for greeting in greeting_patterns):
        return (
            "Hello — I’m **Command Nexus**, RigOS’s refinery operations copilot. "
            "I can help interpret operational procedures, maintenance guidance, "
            "asset conditions, incident response, and safety questions from the "
            "configured knowledge base."
        )

    if "who are you" in normalized:
        return (
            "I’m **Command Nexus**, the RigOS knowledge copilot. For operational "
            "questions, I retrieve the relevant refinery knowledge before answering."
        )

    if "what can you do" in normalized or normalized == "help" or normalized.startswith("help "):
        return (
            "I can help with refinery operations, equipment maintenance, safety "
            "procedures, incidents, and asset questions. Ask an operational question "
            "and I’ll consult the configured knowledge base."
        )

    if normalized in ("thanks", "thank you", "thx") or normalized.startswith("thanks "):
        return "You’re welcome. Ask anytime if you need help with an operational or safety question."

    return None


def _emit(callback: ProgressCallback | None, message: str) -> None:
    """Log and optionally expose a diagnostic stage without changing backend behavior."""
    LOGGER.info(message)
    if callback is not None:
        callback(message)


class KnowledgeAgentUnavailable(RuntimeError):
    """Raised when the existing backend knowledge path cannot serve a query."""


@lru_cache(maxsize=1)
def get_knowledge_agent() -> "KnowledgeAgent":
    """Initialize the existing agent once per Streamlit server process."""
    try:
        # Keep RAG/embedding imports lazy so normal Streamlit page rendering is
        # not blocked until an operator actually submits a Copilot question.
        from agents.knowledge import KnowledgeAgent

        return KnowledgeAgent()
    except Exception as error:
        raise KnowledgeAgentUnavailable(
            "The Knowledge Agent could not initialize. "
            f"Underlying exception: {type(error).__name__}: {error}"
        ) from error


def ask_knowledge_agent(question: str, on_progress: ProgressCallback | None = None) -> str:
    """Return the existing agent's answer for a user question.

    KnowledgeAgent currently exposes ``execute(task)`` directly; it does not
    accept an execution context, so MAO's Executor cannot call it without a
    backend signature change. This adapter intentionally does not create a
    second MAOKernel or replicate any agent/RAG/LLM behavior.
    """
    _emit(on_progress, "Adapter entered ask_knowledge_agent().")
    normalized_question = question.strip()
    if not normalized_question:
        raise KnowledgeAgentUnavailable("Enter a question before querying the Knowledge Agent.")

    conversation = conversational_response(normalized_question)
    if conversation is not None:
        _emit(on_progress, "Conversational intent detected; RAG retrieval not required.")
        return conversation

    _emit(on_progress, "Creating existing MAO Task for the Knowledge Agent.")
    task = Task(
        name="Operator knowledge query",
        description=normalized_question,
        assigned_agent="knowledge",
    )

    try:
        cache_state = "Reusing cached" if get_knowledge_agent.cache_info().currsize else "Initializing"
        _emit(on_progress, f"{cache_state} existing KnowledgeAgent instance.")
        agent = get_knowledge_agent()
        _emit(on_progress, "Calling KnowledgeAgent.execute(Task).")
        result = agent.execute(task)
        _emit(on_progress, f"KnowledgeAgent.execute(Task) returned (success={result.success}).")
    except KnowledgeAgentUnavailable:
        raise
    except Exception as error:
        _emit(on_progress, f"KnowledgeAgent path raised {type(error).__name__}: {error}")
        raise KnowledgeAgentUnavailable(
            f"The Knowledge Agent could not complete this request. "
            f"Underlying exception: {type(error).__name__}: {error}"
        ) from error

    if not result.success or not result.summary:
        raise KnowledgeAgentUnavailable("The Knowledge Agent returned no usable answer.")

    _emit(on_progress, "Returning existing AgentResult.summary to the frontend.")
    return result.summary
