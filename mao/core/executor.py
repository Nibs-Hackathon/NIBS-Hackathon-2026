from mao.models.result import AgentResult
from mao.core.exceptions import AgentNotFound


class Executor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, task, context):

        agent = self.registry.get(
            task.assigned_agent
        )

        if agent is None:
            raise AgentNotFound(
                f"Agent '{task.assigned_agent}' not found."
            )

        try:

            # Agent.run() handles:
            # think()
            # execute()
            # validate_result()
            # reflect()
            result = agent.run(
                task,
                context,
            )

        except Exception as e:

            result = AgentResult(
                agent_name=agent.name,
                success=False,
                finding="Agent execution failed.",
                confidence=0.0,
                summary=str(e),
                recommendations=[
                    "Review execution logs."
                ],
                metadata={
                    "exception": type(e).__name__,
                },
            )

        result.metadata.update(
            {
                "task_name": task.name,
                "task_description": task.description,
                "event_name": context.event.name,
                "asset_id": context.event.source,
            }
        )

        return result