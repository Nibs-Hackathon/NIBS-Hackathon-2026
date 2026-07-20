from mao.event_bus import EventBus
from mao.registry import AgentRegistry
from mao.state import GlobalState


class MAO:

    def __init__(self):

        self.registry = AgentRegistry()

        self.event_bus = EventBus()

        self.state = GlobalState()

    def register_agent(self, agent):

        self.registry.register(agent)

        print(f"[MAO] Registered {agent.name}")

    def publish(self, event):

        self.state.add_event(event)

        self.event_bus.publish(event)

    def run(self):

        print()

        print("========== MAO ==========")

        print("Agents:", len(self.registry.all()))

        print("Events:", len(self.state.events))

        print("=========================")