from patterns.strategy import WorkBehavior, RestBehavior, MoodBehavior


class Creature:
    def __init__(self, name, profession):
        self.name = name
        self.profession = profession
        self.state = "idle"
        self.health = 100
        self.hunger = 0
        self.energy = 100
        self.stress = 0

        # Стратегии поведения
        self.work_behavior: WorkBehavior = None
        self.rest_behavior: RestBehavior = None
        self.mood_behavior: MoodBehavior = None

    def perform_work(self):
        if self.work_behavior:
            self.work_behavior.work(self)

    def perform_rest(self):
        if self.rest_behavior:
            self.rest_behavior.rest(self)

    def perform_mood(self):
        if self.mood_behavior:
            self.mood_behavior.mood(self)

    def set_work_behavior(self, behavior: WorkBehavior):
        self.work_behavior = behavior

    def set_rest_behavior(self, behavior: RestBehavior):
        self.rest_behavior = behavior

    def set_mood_behavior(self, behavior: MoodBehavior):
        self.mood_behavior = behavior

    # Интерфейс для Декоратора
    def getStats(self):
        return {
            "name": self.name,
            "profession": self.profession,
            "state": self.state,
            "health": self.health,
            "hunger": self.hunger,
            "energy": self.energy,
            "stress": self.stress,
            "work_efficiency": 1.0,
        }

    # Метод для паттерна Команда/Адаптер: обычное существо может принимать задачу напрямую.
    def execute_task(self, task):
        print(f"{self.name} принимает задачу через интерфейс исполнителя: {task.type}")
        self.perform_work()

    def __repr__(self):
        return f"Creature(name={self.name!r}, profession={self.profession!r}, state={self.state!r})"
