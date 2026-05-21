from abc import ABC, abstractmethod
from models.resource import ResourceState
from patterns.singleton import GameLogger


class Observer(ABC):
    @abstractmethod
    def update(self, subject, message):
        pass


class Subject:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(self, message)


class ResourceManager(Subject):
    """Основной субъект Наблюдателя: хранит ресурсы и уведомляет интерфейс/AI/статистику."""

    def __init__(self, initial=None):
        super().__init__()
        self.resources = {}
        if initial:
            for key, amount in initial.items():
                self.resources[key] = ResourceState(key, amount)

    def get_resource_state(self, key):
        return self.resources.get(key)

    def set_resource_state(self, key, amount):
        self.resources[key] = ResourceState(key, amount)
        self.notify_observers(f"Ресурс {key} установлен: {amount}")

    def add(self, key, value):
        self.resources.setdefault(key, ResourceState(key, 0)).add(value)
        self.notify_observers(f"Ресурс {key} изменился: +{value}, всего {self.resources[key].amount}")
        return True

    def spend(self, key, value):
        self.resources.setdefault(key, ResourceState(key, 0))
        ok = self.resources[key].spend(value)
        if ok:
            self.notify_observers(f"Ресурс {key} изменился: -{value}, всего {self.resources[key].amount}")
        else:
            self.notify_observers(f"Недостаточно ресурса {key}: нужно {value}, есть {self.resources[key].amount}")
        return ok

    def items(self):
        return self.resources.items()

    def values(self):
        return self.resources.values()

    def __getitem__(self, key):
        return self.resources[key]


class HUDResourcePanel(Observer):
    def update(self, subject, message):
        print(f"[HUD] {message}")


class BuildingPanel(Observer):
    def update(self, subject, message):
        if "wood" in message or "stone" in message or "Недостаточно" in message:
            print("[BuildingPanel] Проверка доступности строительства")


class CreatureAIObserver(Observer):
    def __init__(self, creature=None):
        self.creature = creature

    def update(self, subject, message):
        if self.creature and "food" in message:
            print(f"[CreatureAI] {self.creature.name} заметил изменение еды и может изменить поведение")


class StatisticsPanel(Observer):
    def update(self, subject, message):
        GameLogger().log("observer", f"StatisticsPanel получил событие: {message}")


# Старый простой менеджер оставлен для совместимости.
class EventManager:
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        self.listeners.append(listener)

    def notify(self, message):
        for listener in self.listeners:
            listener.update(self, message)
