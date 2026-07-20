from mao import MAOKernel
from mao.events.event import Event

from tests.mock_agent import MockAgent
from tests.mock_workflow import MockWorkflow

kernel = MAOKernel()

kernel.register_agent(MockAgent())
kernel.register_workflow(MockWorkflow())

event = Event(
    name="PressureSpike",
    source="Pump-A",
    payload={"pressure": 120},
)

report = kernel.handle_event(event)

print(report)