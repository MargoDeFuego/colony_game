from abc import ABC, abstractmethod
from models.building import Building
from models.task import Task
from patterns.factory_method import create_creature_by_profession
from patterns.singleton import GameLogger


class ElementGenerationTemplate(ABC):
    """Шаблонный метод генерации элементов системы."""

    def generate(self):
        element_type = self.select_type()
        element = self.create_base(element_type)
        self.set_parameters(element)
        self.save_element(element)
        return element

    @abstractmethod
    def select_type(self):
        pass

    @abstractmethod
    def create_base(self, element_type):
        pass

    @abstractmethod
    def set_parameters(self, element):
        pass

    def save_element(self, element):
        GameLogger().log("template_method", f"Сгенерирован элемент: {element}")


class CreatureGenerator(ElementGenerationTemplate):
    def select_type(self):
        return "фермер"

    def create_base(self, element_type):
        return create_creature_by_profession("Сгенерированный житель", element_type)

    def set_parameters(self, element):
        element.hunger = 5
        element.energy = 90
        element.state = "idle"


class BuildingGenerator(ElementGenerationTemplate):
    def select_type(self):
        return "Склад"

    def create_base(self, element_type):
        return Building(element_type)

    def set_parameters(self, element):
        element.level = 1
        element.durability = 100
        element.progress = 10
        element.state = "working"


class TaskGenerator(ElementGenerationTemplate):
    def select_type(self):
        return "build"

    def create_base(self, element_type):
        return Task(element_type, priority=2)

    def set_parameters(self, element):
        element.status = "generated"
        element.progress = 0
