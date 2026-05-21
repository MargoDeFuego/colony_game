class Building:
    """Игровое здание. Используется в БД, Компоновщике и Заместителе."""

    def __init__(self, name, level=1, durability=100, progress=0, state="working"):
        self.name = name
        self.level = level
        self.durability = durability
        self.progress = progress
        self.state = state

    def info(self):
        return {
            "name": self.name,
            "level": self.level,
            "durability": self.durability,
            "progress": self.progress,
            "state": self.state,
        }

    def __repr__(self):
        return f"Building(name={self.name!r}, state={self.state!r}, progress={self.progress})"
