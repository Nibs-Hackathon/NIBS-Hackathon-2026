from unittest.mock import MagicMock

from agents.knowledge import KnowledgeAgent

from mao.models.task import Task


def test_knowledge():

    retriever = MagicMock()

    retriever.retrieve.return_value = []

    vector_store = MagicMock()

    agent = KnowledgeAgent(vector_store)

    agent.retriever = retriever

    from mao.core.context import ExecutionContext


    class Event:
        payload = {}


    context = ExecutionContext(
        Event(),
        None,
        None,
        None,
    )

    result = agent.run(
        Task(
            name="Knowledge",
            description="Retrieve knowledge",
            assigned_agent="knowledge",
            priority=5,
        ),
        context,
    )

    assert result.success

    assert "knowledge" in context.metadata