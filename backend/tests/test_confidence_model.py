from types import SimpleNamespace

from mao.core.context import ExecutionContext
from mao.events.event import Event
from mao.models.result import AgentResult


def _context(signal, value, threshold_name, threshold):
    context = ExecutionContext(
        event=Event(
            name="TestIncident",
            source="asset-1",
            payload={signal: value},
        ),
        state_manager=SimpleNamespace(),
        memory_manager=SimpleNamespace(),
        logger=SimpleNamespace(),
    )
    context.metadata["sensor"] = {
        "signals": {signal: value},
        "thresholds": {threshold_name: threshold},
        "history_samples": 100,
    }
    for index in range(4):
        context.add_result(
            AgentResult(
                agent_name=f"agent-{index}",
                success=True,
                confidence=0.94,
                evidence=["evidence"],
            )
        )
    return context


def test_confidence_varies_with_incident_evidence_strength():
    slight_pressure_spike = _context("pressure", 155, "pressure_max", 150)
    strong_gas_leak = _context("gas", 60, "gas_max", 40)

    pressure_confidence = slight_pressure_spike.execution_metrics[
        "average_confidence"
    ]
    gas_confidence = strong_gas_leak.execution_metrics["average_confidence"]

    assert gas_confidence > pressure_confidence
    assert (
        strong_gas_leak.metadata["confidence_model"]["components"][
            "anomaly_clarity"
        ]
        > slight_pressure_spike.metadata["confidence_model"]["components"][
            "anomaly_clarity"
        ]
    )
