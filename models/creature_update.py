from abc import ABC, abstractmethod
from patterns.command import (
    GatherWoodCommand,
    FarmCommand,
    HuntCommand,
    BuildCommand,
    DestroyCommand,
    RestCommand,
    EatCommand,
)
from patterns.decorators import WellFedEffect, StressedEffect, InspiredEffect
from patterns.singleton import GameLogger, DB_PATH
import sqlite3


class CreatureUpdateTemplate(ABC):
    """Шаблонный метод обновления существа: порядок шагов фиксирован."""

    def update_creature(self, creature, resources):
        self.collect_parameters(creature)
        self.apply_math_model(creature)
        self.choose_behavior(creature, resources)
        self.perform_behavior(creature, resources)
        self.apply_effects(creature)
        self.update_mood(creature)
        self.save_state(creature)

    @abstractmethod
    def collect_parameters(self, creature):
        pass

    @abstractmethod
    def apply_math_model(self, creature):
        pass

    @abstractmethod
    def choose_behavior(self, creature, resources):
        pass

    @abstractmethod
    def perform_behavior(self, creature, resources):
        pass

    @abstractmethod
    def apply_effects(self, creature):
        pass

    @abstractmethod
    def update_mood(self, creature):
        pass

    @abstractmethod
    def save_state(self, creature):
        pass


class DefaultCreatureUpdate(CreatureUpdateTemplate):
    def collect_parameters(self, creature):
        print(f"Сбор параметров: hunger={creature.hunger}, energy={creature.energy}, stress={creature.stress}")

    def apply_math_model(self, creature):
        # energy(t+1) = energy(t) + k1*rest - k2*work
        # stress(t+1) = stress(t) + k3*work - k4*rest
        # hunger растет каждый тик.
        creature.hunger = min(creature.hunger + 10, 100)
        creature.energy = max(creature.energy - 5, 0)
        if creature.state == "work":
            creature.stress = min(creature.stress + 5, 100)
        elif creature.state == "rest":
            creature.stress = max(creature.stress - 5, 0)

    def choose_behavior(self, creature, resources):
        if creature.hunger >= 80:
            creature.state = "hungry"
        elif creature.energy < 30 or creature.stress > 70:
            creature.state = "rest"
        else:
            creature.state = "work"

    def perform_behavior(self, creature, resources):
        command = None
        if creature.state == "hungry":
            command = EatCommand(creature, resources)
        elif creature.state == "rest":
            command = RestCommand(creature)
        elif creature.state == "work":
            if creature.profession == "строитель":
                command = BuildCommand(creature, resources)
            elif creature.profession == "лесоруб":
                command = GatherWoodCommand(creature, resources)
            elif creature.profession == "фермер":
                command = FarmCommand(creature, resources)
            elif creature.profession == "охотник":
                command = HuntCommand(creature, resources)
            elif creature.profession == "разрушитель":
                command = DestroyCommand(creature, resources)
            else:
                creature.perform_work()

        if command:
            # Требование этапа 3: задачи выполняются через интерфейс Команды.
            command.execute()

    def apply_effects(self, creature):
        decorated = WellFedEffect(creature)
        if creature.stress > 40:
            decorated = StressedEffect(decorated)
        if creature.energy > 50:
            decorated = InspiredEffect(decorated)
        stats = decorated.getStats()
        print(f"Эффекты для {creature.name}: {stats}")

    def update_mood(self, creature):
        if creature.mood_behavior:
            creature.mood_behavior.mood(creature)

    def save_state(self, creature):
        print(f"Состояние {creature.name} сохранено: hunger={creature.hunger}, energy={creature.energy}")
        GameLogger().log("state", f"{creature.name}: {creature.state}, hunger={creature.hunger}, energy={creature.energy}, stress={creature.stress}")
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO CreatureStateHistory(creature_name, state, hunger, energy, stress)
                VALUES (?, ?, ?, ?, ?)
                """,
                (creature.name, creature.state, creature.hunger, creature.energy, creature.stress),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error:
            pass
