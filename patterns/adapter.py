from abc import ABC, abstractmethod


class ITaskExecutor(ABC):
    """Целевой интерфейс, который нужен системе задач."""

    @abstractmethod
    def execute_task(self, task):
        pass


class CreatureTaskExecutor(ITaskExecutor):
    """Адаптер для обычного Creature, чтобы явно привести его к ITaskExecutor."""

    def __init__(self, creature):
        self.creature = creature

    def execute_task(self, task):
        print(f"{self.creature.name} выполняет задачу {task.type} напрямую")
        self.creature.execute_task(task)


class WildBeastCreature:
    """Новый модуль системы. У него чужой интерфейс: act/move/eat вместо execute_task."""

    def __init__(self, name="Дикий зверь"):
        self.name = name

    def act(self):
        print(f"{self.name} охраняет территорию")

    def move(self):
        print(f"{self.name} перемещается к цели")

    def eat(self):
        print(f"{self.name} ест добычу")


class WildBeastTaskAdapter(ITaskExecutor):
    """Объектный адаптер: содержит WildBeastCreature и не меняет его исходный класс."""

    def __init__(self, beast):
        self.beast = beast

    def execute_task(self, task):
        task_type = task.type.lower()
        print(f"Адаптер получил задачу для дикого существа: {task.type}")
        if task_type in ("guard", "guardarea", "охрана"):
            self.beast.act()
        elif task_type in ("moveto", "move", "перейти"):
            self.beast.move()
        elif task_type in ("eatfood", "eat", "еда"):
            self.beast.eat()
        else:
            print(f"{self.beast.name} не знает эту задачу и выполняет базовое действие")
            self.beast.act()


class WildBeastTaskClassAdapter(WildBeastCreature, ITaskExecutor):
    """Классовый адаптер: наследуется от WildBeastCreature и добавляет нужный интерфейс."""

    def execute_task(self, task):
        task_type = task.type.lower()
        print(f"Классовый адаптер получил задачу: {task.type}")
        if task_type in ("guard", "guardarea", "охрана"):
            self.act()
        elif task_type in ("moveto", "move", "перейти"):
            self.move()
        elif task_type in ("eatfood", "eat", "еда"):
            self.eat()
        else:
            self.act()
