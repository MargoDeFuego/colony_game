from abc import ABC, abstractmethod
from patterns.singleton import GameLogger


class TaskCommand(ABC):
    """Интерфейс Команды: все игровые задачи выполняются через execute()."""

    @abstractmethod
    def execute(self):
        pass


class GatherWoodCommand(TaskCommand):
    def __init__(self, creature, resources):
        self.creature = creature
        self.resources = resources

    def execute(self):
        self.creature.perform_work()
        self.resources.add("wood", 3)
        GameLogger().log("command", f"{self.creature.name} выполнил команду GatherWoodCommand")
        print(f"{self.creature.name} добыл дерево (+3 wood)")


class FarmCommand(TaskCommand):
    def __init__(self, creature, resources):
        self.creature = creature
        self.resources = resources

    def execute(self):
        self.creature.perform_work()
        self.resources.add("food", 2)
        GameLogger().log("command", f"{self.creature.name} выполнил команду FarmCommand")
        print(f"{self.creature.name} собрал еду (+2 food)")


class HuntCommand(TaskCommand):
    def __init__(self, creature, resources):
        self.creature = creature
        self.resources = resources

    def execute(self):
        self.creature.perform_work()
        self.resources.add("food", 4)
        self.creature.energy = max(self.creature.energy - 8, 0)
        GameLogger().log("command", f"{self.creature.name} выполнил команду HuntCommand")
        print(f"{self.creature.name} успешно охотился (+4 food)")


class BuildCommand(TaskCommand):
    def __init__(self, creature, resources, building=None):
        self.creature = creature
        self.resources = resources
        self.building = building

    def execute(self):
        self.creature.perform_work()
        if self.resources.spend("wood", 2) and self.resources.spend("stone", 1):
            if self.building:
                self.building.progress = min(self.building.progress + 20, 100)
            GameLogger().log("command", f"{self.creature.name} выполнил команду BuildCommand")
            print(f"{self.creature.name} построил часть здания (-2 wood, -1 stone)")
        else:
            print(f"{self.creature.name} хотел строить, но ресурсов не хватает")


class DestroyCommand(TaskCommand):
    def __init__(self, creature, resources):
        self.creature = creature
        self.resources = resources

    def execute(self):
        self.creature.perform_work()
        self.resources.add("stone", 2)
        GameLogger().log("command", f"{self.creature.name} выполнил команду DestroyCommand")
        print(f"{self.creature.name} разрушил старую постройку (+2 stone)")


class RestCommand(TaskCommand):
    def __init__(self, creature):
        self.creature = creature

    def execute(self):
        self.creature.perform_rest()
        GameLogger().log("command", f"{self.creature.name} выполнил команду RestCommand")


class EatCommand(TaskCommand):
    def __init__(self, creature, resources):
        self.creature = creature
        self.resources = resources

    def execute(self):
        if self.resources.spend("food", 1):
            self.creature.hunger = max(self.creature.hunger - 40, 0)
            self.creature.energy = min(self.creature.energy + 5, 100)
            print(f"{self.creature.name} поел (-1 food)")
        else:
            print("В колонии закончилась еда")
        GameLogger().log("command", f"{self.creature.name} выполнил команду EatCommand")


class AssignTaskCommand(TaskCommand):
    """Команда для любого исполнителя, который имеет execute_task(task). Подходит и для Адаптера."""

    def __init__(self, executor, task):
        self.executor = executor
        self.task = task

    def execute(self):
        self.executor.execute_task(self.task)
        GameLogger().log("command", f"Задача {self.task.type} выполнена через AssignTaskCommand")


class CommandQueue:
    def __init__(self):
        self.queue = []

    def add(self, command):
        self.queue.append(command)

    def run(self):
        while self.queue:
            command = self.queue.pop(0)
            command.execute()
