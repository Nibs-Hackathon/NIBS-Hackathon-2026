from services.runtime import kernel



def get_agents():

    agents = []


    # Registered agents

    registry = kernel.registry


    for name, agent in registry.agents.items():

        result = get_latest_result(name)

        agents.append(
            {
                "Agent": agent.name,

                "Specialty": (
                    agent.__class__.__name__
                    .replace("Agent", "")
                ),

                "State": (
                    "Active"
                    if result
                    else "Ready"
                ),

                "Confidence": (
                    f"{round(result.confidence * 100)}%"
                    if result
                    else "N/A"
                ),

                "Current task": (
                    result.metadata.get(
                        "task_name",
                        "Awaiting task"
                    )
                    if result
                    else "Awaiting task"
                )
            }
        )


    return agents




def get_latest_result(agent_name):

    results = [
        result
        for result in kernel.state.agent_results
        if result.agent_name == agent_name
    ]


    if not results:
        return None


    return results[-1]