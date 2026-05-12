class WorkStrategy:
    def execute(self, creature):
        pass

class GatherWoodStrategy(WorkStrategy):
    def execute(self, creature):
        print(f"{creature.name} собирает дерево")

class BuildStrategy(WorkStrategy):
    def execute(self, creature):
        print(f"{creature.name} строит здание")

class FarmStrategy(WorkStrategy):
    def execute(self, creature):
        print(f"{creature.name} работает на ферме")
