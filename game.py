import sqlite3
import random

# Подключение к базе
conn = sqlite3.connect("colony.db")
cursor = conn.cursor()

# --- Сущности ---
class Creature:
    def __init__(self, name, profession):
        self.name = name
        self.profession = profession
        self.state = "idle"
        self.health = 100
        self.hunger = 0
        self.energy = 100


    def assign_task(self, task):
        self.state = f"doing {task}"
        print(f"{self.name} выполняет задачу: {task}")

class ResourceState:
    def __init__(self, type, amount=0):
        self.type = type
        self.amount = amount

    def add(self, value):
        self.amount += value

    def spend(self, value):
        if self.amount >= value:
            self.amount -= value
            return True
        return False

# --- Игровая логика ---
class ColonyGame:

    def __init__(self):

        self.day = 1

        # список поселенцев
        self.creatures = []

        # ресурсы
        self.resources = {
            "wood": ResourceState("wood", 10),
            "stone": ResourceState("stone", 5),
            "food": ResourceState("food", 20),
            "energy": ResourceState("energy", 10),
        }

    def add_creature(self, name, profession):

        c = Creature(name, profession)

        self.creatures.append(c)

        return c

    def render(self):

        print("\n====================")
        print(f"День {self.day}")
        print("====================")

        print("\nРесурсы:")

        for resource in self.resources.values():
            print(f"{resource.type}: {resource.amount}")

        print("\nПоселенцы:")

        for creature in self.creatures:
          print(
                 f"{creature.name} | "
                 f"{creature.profession} | "
                 f"{creature.state} | "
                 f"hunger: {creature.hunger} | "
                 f"energy: {creature.energy}"
           )

    def tick(self):

     print("\n--- Новый день ---")

     for c in self.creatures:

        # голод растет
        c.hunger += 15

        # энергия уменьшается
        c.energy -= 5

        # проверка голода
        if c.hunger >= 80:

            c.state = "hungry"

            print(f"{c.name} голоден и ищет еду!")

            # если есть еда
            if self.resources["food"].amount > 0:

                self.resources["food"].amount -= 1

                c.hunger -= 40

                print(f"{c.name} поел.")

            else:
                print("В колонии закончилась еда!")

        else:

            tasks = [
                "собирает дерево",
                "строит дом",
                "отдыхает",
                "ищет ресурсы"
            ]

            task = random.choice(tasks)

            c.assign_task(task)

     self.day += 1

# --- Запуск ---
if __name__ == "__main__":

    game = ColonyGame()

    game.add_creature("Иван", "строитель")
    game.add_creature("Мария", "фермер")

    while True:

        game.render()

        command = input("\nВведите команду (next/exit): ")

        if command == "next":
            game.tick()

        elif command == "exit":
            break

 
