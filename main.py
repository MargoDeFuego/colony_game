from game import ColonyGame


COMMANDS = {
    "next": {
        "number": "1",
        "title": "Следующий игровой день",
        "aliases": ["1", "дальше", "следующий день", "следующий"],
    },
    "adapter": {
        "number": "2",
        "title": "Проверить модуль адаптера",
        "aliases": ["2", "адаптер"],
    },
    "proxy": {
        "number": "3",
        "title": "Проверить заместитель для клиентской версии",
        "aliases": ["3", "заместитель"],
    },
    "composite": {
        "number": "4",
        "title": "Показать иерархию объектов колонии",
        "aliases": ["4", "компоновщик", "иерархия"],
    },
    "generate": {
        "number": "5",
        "title": "Сгенерировать игровые элементы",
        "aliases": ["5", "генерация", "сгенерировать"],
    },
    "facade": {
        "number": "6",
        "title": "Запустить систему через фасад",
        "aliases": ["6", "фасад"],
    },
    "factory": {
        "number": "7",
        "title": "Создать существ через фабрики",
        "aliases": ["7", "фабрика", "фабрики"],
    },
    "exit": {
        "number": "0",
        "title": "Выход из игры",
        "aliases": ["0", "выход", "выйти"],
    },
}


def show_menu():
    print("\nДоступные действия:")
    for command_data in COMMANDS.values():
        print(f"{command_data['number']}. {command_data['title']}")


def get_command(user_input):
    user_input = user_input.strip().lower()

    for command_key, command_data in COMMANDS.items():
        if user_input in command_data["aliases"]:
            return command_key

    return None


def main():
    game = ColonyGame()

    game.add_creature("Иван", "строитель")
    game.add_creature("Мария", "фермер")
    game.add_creature("Олег", "охотник")
    game.add_creature("Джон", "разрушитель")
    game.add_creature("Анна", "лесоруб")

    while True:
        game.render()
        show_menu()

        user_input = input("\nВведите номер или название действия: ")
        command = get_command(user_input)

        if command == "next":
            game.tick()

        elif command == "adapter":
            game.demo_adapter()

        elif command == "proxy":
            game.demo_proxy()

        elif command == "composite":
            game.demo_composite()

        elif command == "generate":
            game.demo_generation()

        elif command == "facade":
            game.demo_facade()

        elif command == "factory":
            game.demo_factory()

        elif command == "exit":
            print("Игра завершена.")
            break

        else:
            print("Неизвестная команда. Выберите действие из списка.")


if __name__ == "__main__":
    main()