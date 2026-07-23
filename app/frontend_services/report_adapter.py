from services.runtime import kernel


def get_reports():

    reports = kernel.state.execution_reports


    formatted_reports = []


    for report in reports:

        formatted_reports.append(
            {
                "Report": report.id[:8],

                "Title": report.workflow_name,

                "Workflow": report.workflow_name,

                "Status": (
                    "Completed"
                    if report.success
                    else "Escalated"
                ),

                "Generated": report.completed_at.strftime(
                    "%d %b %H:%M"
                ),
            }
        )


    preview = {}


    if reports:

        latest = reports[-1]


        preview = {
            "Report": latest.id[:8],

            "Title": latest.workflow_name,

            "Summary": latest.final_summary,

            "Recommendation": (
                "\n".join(
                    latest.recommendations
                )
                if latest.recommendations
                else "No recommendation generated."
            )
        }


    metrics = [

        (
            "Reports generated",
            str(len(reports)),
            "From MAO executions",
            "cyan"
        ),

        (
            "Resolved incidents",
            str(
                sum(
                    1
                    for r in reports
                    if r.success
                )
            ),
            "Successful workflows",
            "green"
        ),

        (
            "Average response",
            calculate_average_time(reports),
            "Execution duration",
            "green"
        ),

        (
            "Pending review",
            str(
                sum(
                    1
                    for r in reports
                    if not r.success
                )
            ),
            "Requires attention",
            "amber"
        )
    ]


    return {
        "metrics": metrics,
        "reports": formatted_reports,
        "preview": preview,
    }



def calculate_average_time(reports):

    if not reports:
        return "N/A"


    durations = []

    for report in reports:

        duration = (
            report.completed_at
            -
            report.started_at
        ).total_seconds()


        durations.append(duration)


    avg = sum(durations) / len(durations)


    return f"{round(avg,1)} sec"