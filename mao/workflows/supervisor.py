from collections import OrderedDict

from mao.models.result import AgentResult


class Supervisor:
    """
    Aggregates agent outputs into a final decision.
    """

    def summarize(self, results: list[AgentResult]) -> dict:

        if not results:
            return {
                "success": True,
                "confidence": 0.0,
                "summary": "No agents were executed.",
                "recommendations": [],
            }

        success = all(result.success for result in results)

        confidence = (
            sum(result.confidence for result in results)
            / len(results)
        )

        recommendations = list(
            OrderedDict.fromkeys(
                rec
                for result in results
                for rec in result.recommendations
            )
        )

        summary = "\n".join(
            f"[{result.agent_name}] {result.summary}"
            for result in results
        )

        return {
            "success": success,
            "confidence": round(confidence, 2),
            "summary": summary,
            "recommendations": recommendations,
        }