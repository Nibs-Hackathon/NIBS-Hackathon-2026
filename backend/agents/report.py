"""Report aggregation agent with dynamic formatting."""

from __future__ import annotations

from collections import OrderedDict
from datetime import datetime

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class ReportAgent(Agent):
    """Compile prior AgentResult objects with dynamic formatting."""

    name = "report"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        prior_results = list(context.results)
        
        # ✅ Get dynamic workflow sequence for context
        incident_type = getattr(task, "name", "default")
        agent_sequence = self.config.get_workflow_sequence(incident_type)
        
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
        
        # ✅ Add execution trace
        execution_trace = [
            f"{i+1}. {agent_name}"
            for i, agent_name in enumerate(agent_sequence)
        ]
        
        metadata = {
            "source_agents": [result.agent_name for result in prior_results],
            "result_count": len(prior_results),
            "agent_sequence": agent_sequence,  # ✅ Track sequence used
            "execution_trace": execution_trace,
            "completed_at": datetime.now().isoformat(),
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
            summary=f"Report compiled with {len(prior_results)} results. Sequence: {' → '.join(agent_sequence)}",
        )