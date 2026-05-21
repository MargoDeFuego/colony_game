# Этап 3 и Этап 4 — пояснение реализации

## Этап 3

### Новый модуль через Адаптер

Файл: `patterns/adapter.py`

Добавлен новый модуль `WildBeastCreature`. Он не подходит к системе задач напрямую, потому что у него методы:

- `act()`
- `move()`
- `eat()`

А система задач ожидает интерфейс:

- `execute_task(task)`

Поэтому добавлены адаптеры:

- `WildBeastTaskAdapter` — объектный адаптер, содержит объект `WildBeastCreature`.
- `WildBeastTaskClassAdapter` — классовый адаптер, наследуется от `WildBeastCreature`.

Демонстрация запускается командой:

```bash
adapter
```

### Наблюдатель

Файл: `patterns/observer.py`

Субъект:

- `ResourceManager`

Наблюдатели:

- `HUDResourcePanel`
- `BuildingPanel`
- `CreatureAIObserver`
- `StatisticsPanel`

Когда ресурсы меняются, `ResourceManager` автоматически вызывает `notify_observers()`.

### Команда

Файл: `patterns/command.py`

Общий интерфейс:

- `TaskCommand`

Команды:

- `BuildCommand`
- `GatherWoodCommand`
- `FarmCommand`
- `HuntCommand`
- `DestroyCommand`
- `RestCommand`
- `EatCommand`
- `AssignTaskCommand`

В файле `models/creature_update.py` выполнение работы сделано через команды. Это значит, что `tick()` не выполняет работу напрямую, а создает нужную команду и вызывает `execute()`.

### Генерация элементов через Шаблонный метод

Файл: `patterns/template_method.py`

Общий шаблон:

- `ElementGenerationTemplate.generate()`

Шаги шаблона:

1. `select_type()`
2. `create_base()`
3. `set_parameters()`
4. `save_element()`

Конкретные генераторы:

- `CreatureGenerator`
- `BuildingGenerator`
- `TaskGenerator`

Демонстрация запускается командой:

```bash
generate
```

## Этап 4

### Заместитель

Файл: `patterns/proxy.py`

Интерфейс:

- `IBuilding`

Реальный объект:

- `RealBuilding`

Заместитель:

- `BuildingProxy`

`BuildingProxy` создает `RealBuilding` только при первом обращении. Это соответствует диаграмме, где Proxy хранит ссылку на реальное здание и выполняет ленивую загрузку.

Демонстрация запускается командой:

```bash
proxy
```

### Состояние

Файл: `patterns/state.py`

Состояния здания:

- `StateA_Working`
- `StateB_Damaged`
- `StateC_Overloaded`
- `StateD_Upgrading`
- `StateE_EconomyMode`

`RealBuilding` делегирует поведение текущему состоянию.

### Компоновщик

Файл: `patterns/composite.py`

Общие элементы:

- `ColonyComponent`
- `ColonyGroup`
- `ColonyLeaf`

Через них создается дерево:

```text
Micro-Colony
├── Существа
└── Здания
```

### Итератор

Файлы:

- `patterns/iterator.py`
- `patterns/composite.py`

Для существ:

- `CreatureCollection`
- `CreatureIterator`

Для дерева Компоновщика:

- `CompositeIterator`

В `ColonyGame.tick()` существа обходятся именно через `CreatureIterator`, как на схеме с `ICreatureIterator`.

## База данных

Файл: `init_db.py`

База создается в:

```text
database/colony.db
```

Создаются таблицы:

- `Creature`
- `ResourceState`
- `Building`
- `Task`
- `CreatureStateHistory`
- `GameEventLog`

Стартовое заполнение содержит больше 20 записей.
