from datetime import datetime
from uuid import uuid4
from typing import Any, Dict, List, Optional


class ExecutionContext:

    def __init__(
        self,
        event,
        state_manager,
        memory_manager,
        logger,
        health_service=None,
    ):

        # Unique execution information
        self.execution_id = str(uuid4())
        self.started_at = datetime.now()

        # Event information
        self.event = event
        self.workflow = None

        # Shared services
        self.state = state_manager
        self.memory = memory_manager
        self.logger = logger
        self.health_service = health_service

        # Agent execution
        self.results: List[Any] = []
        self.last_result: Optional[Any] = None

        # Shared knowledge between agents
        self.shared_evidence: List[str] = []
        self.shared_recommendations: List[str] = []

        # Incident state
        self.incident_level: Optional[str] = None
        self.requires_shutdown: bool = False
        self.requires_human_approval: bool = False

        # Runtime metrics
        self.execution_metrics: Dict[str, Any] = {
            "agents_executed": 0,
            "successful_agents": 0,
            "failed_agents": 0,
            "average_confidence": 0.0,
        }

        # Flexible storage for workflows/agents
        self.metadata: Dict[str, Any] = {}

    def add_result(self, result):
        """
        Register an agent result and update execution state.
        """

        self.results.append(result)
        self.last_result = result

        if result.evidence:
            self.shared_evidence.extend(result.evidence)

        if result.recommendations:
            self.shared_recommendations.extend(result.recommendations)

        self.execution_metrics["agents_executed"] += 1

        if result.success:
            self.execution_metrics["successful_agents"] += 1
        else:
            self.execution_metrics["failed_agents"] += 1

        if result.requires_human_approval:
            self.requires_human_approval = True

        if self.results:
            self.execution_metrics["average_confidence"] = (
                self._calculate_evidence_confidence()
            )

    def _calculate_evidence_confidence(self) -> float:
        """Calculate deterministic confidence from evidence quality.

        Agent self-confidence remains one input, but it cannot dominate the
        incident score. Telemetry coverage, successful-agent agreement,
        evidence coverage, and the observed threshold margin make otherwise
        similar workflows produce incident-specific confidence values.
        """
        results = self.results
        agent_mean = sum(float(result.confidence) for result in results) / len(results)
        success_ratio = sum(bool(result.success) for result in results) / len(results)
        evidence_coverage = (
            sum(bool(result.evidence) for result in results) / len(results)
        )

        sensor = self.metadata.get("sensor", {})
        history_samples = max(0, int(sensor.get("history_samples", 0) or 0))
        telemetry_quality = min(1.0, history_samples / 100)
        anomaly_clarity = self._anomaly_clarity(
            sensor.get("signals", {}),
            sensor.get("thresholds", {}),
        )

        components = {
            "agent_mean": round(agent_mean, 4),
            "telemetry_quality": round(telemetry_quality, 4),
            "agent_agreement": round(success_ratio, 4),
            "evidence_coverage": round(evidence_coverage, 4),
            "anomaly_clarity": round(anomaly_clarity, 4),
        }
        score = (
            components["agent_mean"] * 0.35
            + components["telemetry_quality"] * 0.20
            + components["agent_agreement"] * 0.20
            + components["evidence_coverage"] * 0.10
            + components["anomaly_clarity"] * 0.15
        )
        confidence = round(max(0.0, min(0.99, score)), 4)
        self.metadata["confidence_model"] = {
            "method": "evidence_weighted_v1",
            "components": components,
            "confidence": confidence,
        }
        return confidence

    @staticmethod
    def _anomaly_clarity(signals: dict, thresholds: dict) -> float:
        mappings = (
            ("pressure", "pressure_max", "high"),
            ("temperature", "temperature_max", "high"),
            ("gas", "gas_max", "high"),
            ("gas_level", "gas_max", "high"),
            ("vibration", "vibration_max", "high"),
            ("flow", "flow_min", "low"),
        )
        margins = []
        for signal_name, threshold_name, direction in mappings:
            if signal_name not in signals or threshold_name not in thresholds:
                continue
            try:
                observed = float(signals[signal_name])
                threshold = float(thresholds[threshold_name])
            except (TypeError, ValueError):
                continue
            if threshold == 0:
                continue
            deviation = (
                observed - threshold
                if direction == "high"
                else threshold - observed
            )
            margins.append(max(0.0, min(1.0, deviation / abs(threshold))))

        if not margins:
            return 0.45 if signals else 0.20
        return min(1.0, 0.55 + max(margins) * 0.45)
