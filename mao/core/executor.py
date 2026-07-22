from mao.models.result import AgentResult
from mao.core.exceptions import AgentNotFound


class Executor:

    def __init__(self, registry):
        self.registry = registry

<<<<<<< HEAD
    def execute(self, task):
=======
    def execute(self, task, context):
>>>>>>> origin/dev-ashutosh-zinia

        agent = self.registry.get(task.assigned_agent)

        if agent is None:
            raise AgentNotFound(
                f"Agent '{task.assigned_agent}' not found."
            )

        # Agent lifecycle
        agent.think(task)

        try:
<<<<<<< HEAD
            result = agent.execute(task)
=======
            result = agent.execute(task, context)
>>>>>>> origin/dev-ashutosh-zinia

        except Exception as e:

            result = AgentResult(
                agent_name=agent.name,
                success=False,
                confidence=0.0,
                summary=str(e),
                recommendations=[],
            )

        agent.reflect(result)

        return result