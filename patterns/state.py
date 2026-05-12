class CreatureState:

    def handle(self, creature):
        pass

class WorkingState(CreatureState):

    def handle(self, creature):
        creature.energy -= 10

class RestingState(CreatureState):

    def handle(self, creature):
        creature.energy += 15
