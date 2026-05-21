from abc import ABC, abstractmethod


class ColonyComponent(ABC):
    """Общий компонент Компоновщика."""

    @abstractmethod
    def show(self, indent=0):
        pass


class ColonyLeaf(ColonyComponent):
    def __init__(self, name, object_type, payload=None):
        self.name = name
        self.object_type = object_type
        self.payload = payload

    def show(self, indent=0):
        print(" " * indent + f"- {self.object_type}: {self.name}")


class ColonyGroup(ColonyComponent):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def show(self, indent=0):
        print(" " * indent + f"+ Группа: {self.name}")
        for child in self.children:
            child.show(indent + 2)

    def create_iterator(self):
        return CompositeIterator(self)


class CompositeIterator:
    """Итератор для обхода дерева Компоновщика в глубину."""

    def __init__(self, root):
        self.items = []
        self.index = -1
        self._flatten(root)

    def _flatten(self, component):
        self.items.append(component)
        if isinstance(component, ColonyGroup):
            for child in component.children:
                self._flatten(child)

    def move_next(self):
        if self.index + 1 < len(self.items):
            self.index += 1
            return True
        return False

    def current(self):
        if 0 <= self.index < len(self.items):
            return self.items[self.index]
        return None

    def reset(self):
        self.index = -1
