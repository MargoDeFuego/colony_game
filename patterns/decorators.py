# patterns/decorators.py
# Паттерн Декоратор: эффекты временно меняют характеристики Creature без изменения исходного класса.

class CreatureDecorator:
    def __init__(self, creature):
        self.creature = creature

    def getStats(self):
        return self.creature.getStats()


class WellFedEffect(CreatureDecorator):
    def getStats(self):
        stats = super().getStats()
        stats["energy"] = min(stats["energy"] * 1.1, 100)
        return stats


class StressedEffect(CreatureDecorator):
    def getStats(self):
        stats = super().getStats()
        stats["stress"] = stats.get("stress", 0) + 20
        return stats


class InspiredEffect(CreatureDecorator):
    def getStats(self):
        stats = super().getStats()
        stats["work_efficiency"] = stats.get("work_efficiency", 1.0) * 1.15
        return stats


class PoisonedEffect(CreatureDecorator):
    def getStats(self):
        stats = super().getStats()
        stats["energy"] = max(stats["energy"] - 5, 0)
        return stats
