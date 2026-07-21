from agents.knowledge import KnowledgeAgent


agent = KnowledgeAgent()


class Task:

    description = (
        "What should operators do during a pressure spike?"
    )


result = agent.execute(Task())


print("="*60)
print(result.summary)
print("="*60)