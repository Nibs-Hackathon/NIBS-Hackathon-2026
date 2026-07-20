from mao.event_bus import EventBus
from mao.registry import AgentRegistry
from mao.state import GlobalState
from mao.planner import Planner


class MAO:

    def __init__(self):

        self.registry = AgentRegistry()

        self.event_bus = EventBus()

        self.state = GlobalState()
        self.planner = Planner()

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
    
    def handle_event(self, event):
        self.publish(event)

        tasks = self.planner.create_plan(event)

        for task in tasks:
            self.state.enequeue_task(task)

        while True:
            task = self.state.next_task()
            if task is None:
                break
            self.registry.dispatch(task)



