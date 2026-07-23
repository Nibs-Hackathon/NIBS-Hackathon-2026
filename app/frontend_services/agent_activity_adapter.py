from services.runtime import kernel
from datetime import datetime


def get_agent_activity():

    results = kernel.state.agent_results

    activities = []


    for result in results:

        activities.append(
            {
                "time": datetime.now().strftime(
                    "%H:%M:%S"
                ),

                "agent": result.agent_name,

                "action": (
                    result.summary
                    if result.summary
                    else result.finding
                ),

                "state": (
                    "Completed"
                    if result.success
                    else "Failed"
                ),

                "confidence": (
                    f"{round(result.confidence * 100)}%"
                ),

                "progress": 100
            }
        )


    return activities



def get_agent_metrics():

    results = kernel.state.agent_results


    if not results:

        return [
            (
                "Activities today",
                "0",
                "Waiting for execution",
                "cyan"
            ),

            (
                "Completed workflows",
                "0",
                "No executions",
                "green"
            ),

            (
                "Human reviews",
                "0",
                "No pending review",
                "amber"
            ),

            (
                "Avg confidence",
                "0%",
                "No data",
                "violet"
            )
        ]


    completed = sum(
        1
        for r in results
        if r.success
    )


    confidence = (
        sum(
            r.confidence
            for r in results
        )
        /
        len(results)
    )


    reviews = sum(
        1
        for r in results
        if r.requires_human_approval
    )


    return [

        (
            "Activities today",
            str(len(results)),
            "From MAO execution",
            "cyan"
        ),

        (
            "Completed workflows",
            str(completed),
            "Successful executions",
            "green"
        ),

        (
            "Human reviews",
            str(reviews),
            "Approval required",
            "amber"
        ),

        (
            "Avg confidence",
            f"{round(confidence*100,1)}%",
            "Agent confidence",
            "violet"
        )
    ]