from abc import ABC, abstractmethod


class ICreatureIterator(ABC):
    @abstractmethod
    def current(self):
        pass

    @abstractmethod
    def move_next(self):
        pass

    @abstractmethod
    def reset(self):
        pass


class CreatureIterator(ICreatureIterator):
    """Конкретный итератор для безопасного последовательного обхода существ."""

    def __init__(self, collection):
        self.collection = collection
        self.index = -1

    def current(self):
        if 0 <= self.index < len(self.collection.creatures):
            return self.collection.creatures[self.index]
        return None

    def move_next(self):
        if self.index + 1 < len(self.collection.creatures):
            self.index += 1
            return True
        return False

    def reset(self):
        self.index = -1


class CreatureCollection:
    """Коллекция существ скрывает внутренний список и выдаёт итератор."""

    def __init__(self):
        self.creatures = []

    def add(self, creature):
        self.creatures.append(creature)

    def create_iterator(self):
        return CreatureIterator(self)

    def __iter__(self):
        return iter(self.creatures)

    def __len__(self):
        return len(self.creatures)

    def __getitem__(self, index):
        return self.creatures[index]
