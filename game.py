from init_db import init_database
from models.creature_update import DefaultCreatureUpdate
from models.task import Task
from patterns.abstract_factory import BalancedColonyFactory
from patterns.adapter import WildBeastCreature, WildBeastTaskAdapter, WildBeastTaskClassAdapter
from patterns.command import AssignTaskCommand
from patterns.composite import ColonyGroup, ColonyLeaf
from patterns.facade import ColonyGameFacade
from patterns.factory_method import create_creature_by_profession
from patterns.iterator import CreatureCollection
from patterns.observer import ResourceManager, HUDResourcePanel, BuildingPanel, CreatureAIObserver, StatisticsPanel
from patterns.proxy import BuildingProxy, get_building_state_by_name
from patterns.singleton import GameLogger
from patterns.template_method import CreatureGenerator, BuildingGenerator, TaskGenerator


class ColonyGame:
    def __init__(self):
        init_database(reset=False, seed=True)
        self.day = 1
        self.creatures = CreatureCollection()
        self.buildings = []
        self.resources = ResourceManager(
            {
                "wood": 10,
                "stone": 5,
                "food": 20,
                "energy": 0,
                "water": 10,
            }
        )
        self.resources.register_observer(HUDResourcePanel())
        self.resources.register_observer(BuildingPanel())
        self.resources.register_observer(StatisticsPanel())
        self.facade = ColonyGameFacade(self)

    def add_creature(self, name, profession):
        creature = create_creature_by_profession(name, profession)
        self.creatures.add(creature)

        # AI существа тоже наблюдатель за ресурсами.
        self.resources.register_observer(CreatureAIObserver(creature))
        return creature

    def add_default_colony_by_abstract_factory(self):
        """Демонстрация Абстрактной фабрики."""
        factory = BalancedColonyFactory()
        for creature in [
            factory.create_builder("Фабричный строитель"),
            factory.create_farmer("Фабричный фермер"),
            factory.create_hunter("Фабричный охотник"),
        ]:
            self.creatures.add(creature)
        print("Абстрактная фабрика создала семейство существ: строитель, фермер, охотник")

    def render(self):
        print("\n====================")
        print(f"День {self.day}")
        print("====================")

        print("\nРесурсы:")
        for key, resource in self.resources.items():
            print(f"{key}: {resource.amount}")

        print("\nПоселенцы:")
        for creature in self.creatures:
            print(
                f"{creature.name} | "
                f"{creature.profession} | "
                f"{creature.state} | "
                f"hunger: {creature.hunger} | "
                f"energy: {creature.energy} | "
                f"stress: {creature.stress}"
            )

        if self.buildings:
            print("\nЗдания:")
            for building in self.buildings:
                print(f"{building.name} | state={building.state} | progress={building.progress}")

    def tick(self):
        print("\n--- Новый день ---")
        updater = DefaultCreatureUpdate()

        # Этап 4: перебор существ через Iterator, а не прямой обход списка.
        iterator = self.creatures.create_iterator()
        while iterator.move_next():
            creature = iterator.current()
            updater.update_creature(creature, self.resources)

        self.day += 1

    def demo_adapter(self):
        print("\n--- Демонстрация Адаптера ---")
        task_guard = Task("guard", priority=1)
        task_move = Task("moveto", priority=1)
        task_eat = Task("eatfood", priority=1)

        beast = WildBeastCreature("Лесной зверь")
        object_adapter = WildBeastTaskAdapter(beast)
        AssignTaskCommand(object_adapter, task_guard).execute()
        AssignTaskCommand(object_adapter, task_move).execute()

        class_adapter = WildBeastTaskClassAdapter("Пещерный зверь")
        AssignTaskCommand(class_adapter, task_eat).execute()

    def demo_proxy(self):
        print("\n--- Демонстрация Заместителя + Состояния ---")
        proxy = BuildingProxy(1, "Клиентская ферма")
        print("Proxy создан, RealBuilding еще не загружен")
        proxy.set_state(get_building_state_by_name("economy_mode"))
        print(proxy.get_info())
        print(proxy.place())
        print(proxy.do_action())

    def demo_composite(self):
        print("\n--- Демонстрация Компоновщика + Итератора ---")
        colony = ColonyGroup("Micro-Colony")
        creature_group = ColonyGroup("Существа")
        building_group = ColonyGroup("Здания")

        for creature in self.creatures:
            creature_group.add(ColonyLeaf(creature.name, "Creature", creature))

        for building in self.buildings:
            building_group.add(ColonyLeaf(building.name, "Building", building))

        colony.add(creature_group)
        colony.add(building_group)
        colony.show()

        print("\nПоследовательный обход дерева:")
        iterator = colony.create_iterator()
        while iterator.move_next():
            item = iterator.current()
            print(f"-> {item.__class__.__name__}")

    def demo_generation(self):
        print("\n--- Генерация элементов через Шаблонный метод ---")
        creature = CreatureGenerator().generate()
        building = BuildingGenerator().generate()
        task = TaskGenerator().generate()
        self.creatures.add(creature)
        self.buildings.append(building)
        print(f"Создано существо: {creature.name}, profession={creature.profession}")
        print(f"Создано здание: {building.name}, progress={building.progress}")
        print(f"Создана задача: {task.type}, status={task.status}")

    def demo_facade(self):
        print("\n--- Демонстрация Фасада + Заместителя ---")
        self.facade.play()

    def demo_factory(self):
        print("\n--- Демонстрация Фабричного метода и Абстрактной фабрики ---")
        self.add_creature("Созданный фабричным методом", "лесоруб")
        self.add_default_colony_by_abstract_factory()


# --- Запуск ---
if __name__ == "__main__":
    game = ColonyGame()
    game.add_creature("Иван", "строитель")
    game.add_creature("Мария", "фермер")
    game.add_creature("Олег", "охотник")
    game.add_creature("Джон", "разрушитель")
    game.add_creature("Анна", "лесоруб")

    while True:
        game.render()
        command = input(
            "\nВведите команду "
            "(next/adapter/proxy/composite/generate/facade/factory/exit): "
        ).strip().lower()

        if command == "next":
            game.tick()
        elif command == "adapter":
            game.demo_adapter()
        elif command == "proxy":
            game.demo_proxy()
        elif command == "composite":
            game.demo_composite()
        elif command == "generate":
            game.demo_generation()
        elif command == "facade":
            game.demo_facade()
        elif command == "factory":
            game.demo_factory()
        elif command == "exit":
            break
        else:
            print("Неизвестная команда")
