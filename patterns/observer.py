class EventManager:

    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        self.listeners.append(listener)

    def notify(self, message):

        for listener in self.listeners:
            listener.update(message)
