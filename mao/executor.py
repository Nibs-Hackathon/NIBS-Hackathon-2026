class Executor:

    def __init__(self, registry):

        self.registry = registry

    def execute(self, task):

        agent = self.registry.get(task.assigned_agent)

        if not agent:

            raise Exception(
                f"Agent {task.assigned_agent} not found."
            )

        return agent.execute(task)