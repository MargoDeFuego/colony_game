from abc import ABC, abstractmethod
from patterns.state import (
    StateA_Working,
    StateB_Damaged,
    StateC_Overloaded,
    StateD_Upgrading,
    StateE_EconomyMode,
)
from patterns.singleton import GameLogger


class IBuilding(ABC):
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def place(self):
        pass

    @abstractmethod
    def do_action(self):
        pass


class RealBuilding(IBuilding):
    """Настоящее тяжелое здание. В клиентской версии его грузит BuildingProxy."""

    def __init__(self, name, model_data="3D-model", cost=10, workers_required=2):
        self.name = name
        self.model_data = model_data
        self.cost = cost
        self.workers_required = workers_required
        self.state = StateA_Working()

    def set_state(self, state):
        self.state = state

    def render(self):
        return self.state.render(self)

    def get_info(self):
        info = self.state.get_info(self)
        info.update({"cost": self.cost, "workers_required_base": self.workers_required})
        return info

    def place(self):
        return self.state.place(self)

    def do_action(self):
        return self.state.do_action(self)


class BuildingProxy(IBuilding):
    """Заместитель: лениво создает RealBuilding и делегирует ему поведение."""

    def __init__(self, building_id, name):
        self.building_id = building_id
        self.name = name
        self._real_building = None
        self.is_loaded = False

    def _load(self):
        if not self.is_loaded:
            print(f"[Proxy] Ленивая загрузка здания {self.name}")
            self._real_building = RealBuilding(self.name)
            self.is_loaded = True
            GameLogger().log("proxy", f"BuildingProxy загрузил RealBuilding: {self.name}")
        return self._real_building

    def set_state(self, state):
        self._load().set_state(state)

    def render(self):
        return self._load().render()

    def get_info(self):
        return self._load().get_info()

    def place(self):
        return self._load().place()

    def do_action(self):
        return self._load().do_action()


def get_building_state_by_name(name):
    states = {
        "working": StateA_Working,
        "damaged": StateB_Damaged,
        "overloaded": StateC_Overloaded,
        "upgrading": StateD_Upgrading,
        "economy": StateE_EconomyMode,
        "economy_mode": StateE_EconomyMode,
    }
    return states.get(name, StateA_Working)()
