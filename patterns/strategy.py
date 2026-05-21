# patterns/strategy.py
# Паттерн Стратегия: разные алгоритмы работы, отдыха и настроения можно менять у Creature во время игры.

# --- Work Behaviors ---
class WorkBehavior:
    def work(self, creature):
        pass

class GatherWoodWork(WorkBehavior):
    def work(self, creature):
        print(f"{creature.name} собирает дерево")

class BuildWork(WorkBehavior):
    def work(self, creature):
        print(f"{creature.name} строит здание")

class DestroyWork(WorkBehavior):
    def work(self, creature):
        print(f"{creature.name} разрушает здание")

class HuntWork(WorkBehavior):
    def work(self, creature):
        print(f"{creature.name} охотится")

class FarmWork(WorkBehavior):
    def work(self, creature):
        print(f"{creature.name} работает на ферме")

class NoWork(WorkBehavior):
    def work(self, creature):
        print(f"{creature.name} бездельничает")


# --- Rest Behaviors ---
class RestBehavior:
    def rest(self, creature):
        pass

class SleepRest(RestBehavior):
    def rest(self, creature):
        creature.energy = min(creature.energy + 20, 100)
        creature.stress = max(creature.stress - 8, 0)
        print(f"{creature.name} спит и восстанавливает энергию")

class MeditationRest(RestBehavior):
    def rest(self, creature):
        creature.energy = min(creature.energy + 5, 100)
        creature.stress = max(creature.stress - 15, 0)
        print(f"{creature.name} медитирует")

class IdleRest(RestBehavior):
    def rest(self, creature):
        creature.energy = min(creature.energy + 8, 100)
        print(f"{creature.name} просто отдыхает")

class NoRest(RestBehavior):
    def rest(self, creature):
        print(f"{creature.name} не отдыхает")


# --- Mood Behaviors ---
class MoodBehavior:
    def mood(self, creature):
        pass

class HappyMood(MoodBehavior):
    def mood(self, creature):
        print(f"{creature.name} счастлив")

class TiredMood(MoodBehavior):
    def mood(self, creature):
        print(f"{creature.name} устал")

class AngryMood(MoodBehavior):
    def mood(self, creature):
        print(f"{creature.name} злой")

class BoredMood(MoodBehavior):
    def mood(self, creature):
        print(f"{creature.name} скучает")

class StressMood(MoodBehavior):
    def mood(self, creature):
        print(f"{creature.name} в стрессе")
