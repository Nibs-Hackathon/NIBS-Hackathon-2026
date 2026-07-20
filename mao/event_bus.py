from collections import defaultdict


class EventBus:

    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):

        self.subscribers[event_name].append(callback)

    def publish(self, event):

        print(f"[EVENT] {event.name}")

        for callback in self.subscribers[event.name]:

            callback(event)