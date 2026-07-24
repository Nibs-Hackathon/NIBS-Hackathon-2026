"""Test script for KnowledgeAgent."""

from agents.knowledge import KnowledgeAgent
from mao.models.task import Task


def test_knowledge_agent():
    """Test the KnowledgeAgent with a simple query."""
    
    # Create the agent
    agent = KnowledgeAgent()
    
    task = Task(
        name="Knowledge Test",
        description="What should operators do during a pressure spike?",
        assigned_agent="knowledge",
        priority=1,
    )
    
    result = agent.execute(task, context=None)
    
    print("=" * 60)
    print("KnowledgeAgent Test Results")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Confidence: {result.confidence}")
    print(f"Finding: {result.finding}")
    print("\nSummary:")
    print(result.summary)
    print("\nRecommendations:")
    for rec in result.recommendations:
        print(f"  - {rec}")
    print("=" * 60)


if __name__ == "__main__":
    test_knowledge_agent()