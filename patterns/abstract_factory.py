from abc import ABC, abstractmethod
from patterns.factory_method import BuilderCreator, FarmerCreator, HunterCreator, LumberjackCreator


class CreatureFamilyFactory(ABC):
    """Абстрактная фабрика: создает семейство связанных существ для сценария колонии."""

    @abstractmethod
    def create_builder(self, name):
        pass

    @abstractmethod
    def create_farmer(self, name):
        pass

    @abstractmethod
    def create_hunter(self, name):
        pass


class BalancedColonyFactory(CreatureFamilyFactory):
    def create_builder(self, name):
        return BuilderCreator().create_creature(name)

    def create_farmer(self, name):
        return FarmerCreator().create_creature(name)

    def create_hunter(self, name):
        return HunterCreator().create_creature(name)


class SurvivalColonyFactory(CreatureFamilyFactory):
    def create_builder(self, name):
        return LumberjackCreator().create_creature(name)

    def create_farmer(self, name):
        return FarmerCreator().create_creature(name)

    def create_hunter(self, name):
        return HunterCreator().create_creature(name)
