"""Test script for MAO kernel."""

from mao import MAOKernel
from agents.safety import SafetyAgent
from mao.events.event import Event

# Create kernel
kernel = MAOKernel()

# Register agent
safety = SafetyAgent()
kernel.register_agent(safety)

# Create event
event = Event(
    name="PressureSpike",
    source="SensorAgent",
    payload={
        "asset": "Pump A",
        "pressure": 112,
    },
)

# ✅ FIXED: Use handle_event
report = kernel.handle_event(event)

print("=" * 60)
print("MAO Test Results")
print("=" * 60)
print(f"Workflow: {report.workflow_name}")
print(f"Success: {report.success}")
print(f"Summary: {report.final_summary}")
print(f"Confidence: {report.average_confidence}")