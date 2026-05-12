class Creature:

    def __init__(self, name, profession):
        self.name = name
        self.profession = profession
        self.state = "idle"
        self.health = 100
        self.hunger = 0
        self.energy = 100
        