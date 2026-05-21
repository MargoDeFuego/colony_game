from abc import ABC, abstractmethod
from models.creature import Creature
from patterns.strategy import (
    GatherWoodWork,
    BuildWork,
    DestroyWork,
    HuntWork,
    FarmWork,
    NoWork,
    SleepRest,
    MeditationRest,
    IdleRest,
    HappyMood,
    TiredMood,
    AngryMood,
    BoredMood,
    StressMood,
)


class CreatureCreator(ABC):
    """Фабричный метод: подклассы решают, какого Creature создать."""

    @abstractmethod
    def create_creature(self, name):
        pass

    def _set_common_behavior(self, creature):
        creature.set_rest_behavior(SleepRest())
        creature.set_mood_behavior(HappyMood())
        return creature


class BuilderCreator(CreatureCreator):
    def create_creature(self, name):
        creature = Creature(name, "строитель")
        creature.set_work_behavior(BuildWork())
        return self._set_common_behavior(creature)


class FarmerCreator(CreatureCreator):
    def create_creature(self, name):
        creature = Creature(name, "фермер")
        creature.set_work_behavior(FarmWork())
        return self._set_common_behavior(creature)


class HunterCreator(CreatureCreator):
    def create_creature(self, name):
        creature = Creature(name, "охотник")
        creature.set_work_behavior(HuntWork())
        return self._set_common_behavior(creature)


class LumberjackCreator(CreatureCreator):
    def create_creature(self, name):
        creature = Creature(name, "лесоруб")
        creature.set_work_behavior(GatherWoodWork())
        return self._set_common_behavior(creature)


class DestroyerCreator(CreatureCreator):
    def create_creature(self, name):
        creature = Creature(name, "разрушитель")
        creature.set_work_behavior(DestroyWork())
        return self._set_common_behavior(creature)


class DefaultCreatureCreator(CreatureCreator):
    def create_creature(self, name):
        creature = Creature(name, "житель")
        creature.set_work_behavior(NoWork())
        creature.set_rest_behavior(IdleRest())
        creature.set_mood_behavior(BoredMood())
        return creature


def create_creature_by_profession(name, profession):
    creators = {
        "строитель": BuilderCreator(),
        "фермер": FarmerCreator(),
        "охотник": HunterCreator(),
        "лесоруб": LumberjackCreator(),
        "разрушитель": DestroyerCreator(),
    }
    creature = creators.get(profession, DefaultCreatureCreator()).create_creature(name)

    # Для разнообразия оставляем возможность менять стратегии после создания.
    if profession == "строитель":
        creature.set_mood_behavior(TiredMood())
    elif profession == "охотник":
        creature.set_rest_behavior(MeditationRest())
    elif profession == "разрушитель":
        creature.set_mood_behavior(AngryMood())
    elif profession == "лесоруб":
        creature.set_mood_behavior(StressMood())

    return creature
