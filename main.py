from game import ColonyGame

game = ColonyGame()
game.add_creature("Иван", "строитель")
game.add_creature("Мария", "фермер")

while True:
    game.render()
    command = input("> ")

    if command == "next":
        game.tick()
    elif command == "exit":
        break
