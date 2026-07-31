class EventStore:

    def __init__(self):

        self.events = []

    def save(self, event):

        self.events.append(event)

    def all(self):

        return self.events