"""Report aggregation agent using the existing ExecutionReport pipeline."""

from __future__ import annotations

from collections import OrderedDict

from agents.base import Agent
from mao.models.result import AgentResult


class ReportAgent(Agent):
    """Compile prior AgentResult objects for inclusion in ExecutionReport."""

    name = "report"

    def execute(self, task, context):
        prior_results = list(context.results)
        recommendations = list(
            OrderedDict.fromkeys(
                recommendation
                for result in prior_results
                for recommendation in result.recommendations
            )
        )
        evidence = [
            f"{result.agent_name}: {result.finding}"
            for result in prior_results
            if result.finding
        ]
        confidence = (
            round(sum(result.confidence for result in prior_results) / len(prior_results), 2)
            if prior_results
            else 0.0
        )
        metadata = {
            "source_agents": [result.agent_name for result in prior_results],
            "result_count": len(prior_results),
        }
        context.metadata["report"] = metadata

        return AgentResult(
            agent_name=self.name,
            success=all(result.success for result in prior_results),
            finding=f"Compiled {len(prior_results)} agent result(s) for the execution report.",
            confidence=confidence,
            evidence=evidence,
            recommendations=recommendations,
            required_action="Review execution report",
            requires_human_approval=any(
                result.requires_human_approval for result in prior_results
            ),
            metadata=metadata,
            summary="Report inputs compiled for the existing ExecutionReport pipeline.",
        )
