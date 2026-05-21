# Паттерн Состояние.
# CreatureState оставлен для поселенцев, BuildingState добавлен по схеме Заместителя.

class CreatureState:
    def handle(self, creature):
        pass


class WorkingState(CreatureState):
    def handle(self, creature):
        creature.energy = max(creature.energy - 10, 0)
        creature.stress = min(creature.stress + 5, 100)


class RestingState(CreatureState):
    def handle(self, creature):
        creature.energy = min(creature.energy + 15, 100)
        creature.stress = max(creature.stress - 5, 0)


class BuildingState:
    name = "base"
    energy_consumption = 0
    workers_required = 0

    def render(self, building):
        return f"{building.name}: состояние {self.name}"

    def get_info(self, building):
        return {
            "name": building.name,
            "state": self.name,
            "energy_consumption": self.energy_consumption,
            "workers_required": self.workers_required,
        }

    def place(self, building):
        return f"{building.name} размещено в режиме {self.name}"

    def do_action(self, building):
        return f"{building.name} выполняет действие в состоянии {self.name}"


class StateA_Working(BuildingState):
    name = "working"
    energy_consumption = 1
    workers_required = 2


class StateB_Damaged(BuildingState):
    name = "damaged"
    energy_consumption = 0
    workers_required = 0


class StateC_Overloaded(BuildingState):
    name = "overloaded"
    energy_consumption = 3
    workers_required = 4


class StateD_Upgrading(BuildingState):
    name = "upgrading"
    energy_consumption = 2
    workers_required = 0


class StateE_EconomyMode(BuildingState):
    name = "economy_mode"
    energy_consumption = 0.5
    workers_required = 1
