from mao.models.result import AgentResult


class SupervisorAgent:

    def review(self, results: list[AgentResult]):

        overall_confidence = (
            sum(r.confidence for r in results) / len(results)
            if results else 0
        )

        recommendations = []

        for result in results:
            recommendations.extend(result.recommendations)

        return {
            "confidence": round(overall_confidence, 2),
            "recommendations": list(dict.fromkeys(recommendations)),
            "results": results,
        }