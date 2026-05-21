from datetime import datetime


class GameEvent:
    def __init__(self, event_type, description):
        self.event_type = event_type
        self.description = description
        self.created_at = datetime.now()

    def __repr__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M:%S}] {self.event_type}: {self.description}"
