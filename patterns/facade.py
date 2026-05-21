from models.building import Building
from patterns.proxy import BuildingProxy, get_building_state_by_name
from patterns.singleton import GameLogger


class ColonyGameFacade:
    """Фасад клиентской версии: скрывает работу с Proxy, зданиями и размещением."""

    def __init__(self, game):
        self.game = game
        self.selected_building = None

    def build_menu(self):
        print("Меню строительства: Дом, Ферма, Склад, Башня")

    def select_building(self, name="Ферма"):
        building_id = len(self.game.buildings) + 1
        self.selected_building = BuildingProxy(building_id, name)
        print(f"Выбрано здание через фасад: {name}")
        return self.selected_building

    def place_building(self, state="working"):
        if not self.selected_building:
            self.select_building()
        self.selected_building.set_state(get_building_state_by_name(state))
        print(self.selected_building.place())
        print(self.selected_building.render())
        building = Building(self.selected_building.name, state=state)
        self.game.buildings.append(building)
        GameLogger().log("facade", f"Фасад разместил здание {building.name} в состоянии {state}")
        return building

    def play(self):
        self.build_menu()
        self.select_building("Ферма")
        self.place_building("economy_mode")
