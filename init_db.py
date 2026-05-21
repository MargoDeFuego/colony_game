import os
import sqlite3

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "database", "colony.db")


def init_database(reset=False, seed=True):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if reset:
        cursor.executescript(
            """
            DROP TABLE IF EXISTS CreatureStateHistory;
            DROP TABLE IF EXISTS GameEventLog;
            DROP TABLE IF EXISTS Task;
            DROP TABLE IF EXISTS Building;
            DROP TABLE IF EXISTS ResourceState;
            DROP TABLE IF EXISTS Creature;
            """
        )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Creature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            profession TEXT NOT NULL,
            health INTEGER DEFAULT 100,
            hunger INTEGER DEFAULT 0,
            energy INTEGER DEFAULT 100,
            stress INTEGER DEFAULT 0,
            state TEXT DEFAULT 'idle'
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ResourceState (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL UNIQUE,
            amount INTEGER NOT NULL DEFAULT 0
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Building (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            durability INTEGER DEFAULT 100,
            progress INTEGER DEFAULT 0,
            state TEXT DEFAULT 'working',
            energy_consumption REAL DEFAULT 1,
            workers_required INTEGER DEFAULT 1
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            priority INTEGER DEFAULT 1,
            status TEXT DEFAULT 'new',
            building_id INTEGER,
            creature_id INTEGER,
            progress INTEGER DEFAULT 0,
            FOREIGN KEY(building_id) REFERENCES Building(id),
            FOREIGN KEY(creature_id) REFERENCES Creature(id)
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CreatureStateHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creature_name TEXT NOT NULL,
            state TEXT,
            hunger INTEGER,
            energy INTEGER,
            stress INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS GameEventLog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    if seed and _is_empty(cursor):
        seed_database(cursor)

    conn.commit()
    conn.close()
    return DB_PATH


def _is_empty(cursor):
    cursor.execute("SELECT COUNT(*) FROM Creature")
    return cursor.fetchone()[0] == 0


def seed_database(cursor):
    creatures = [
        ("Иван", "строитель", 100, 10, 95, 0, "idle"),
        ("Мария", "фермер", 100, 5, 100, 0, "idle"),
        ("Олег", "охотник", 100, 20, 90, 5, "idle"),
        ("Джон", "разрушитель", 100, 15, 85, 10, "idle"),
        ("Анна", "лесоруб", 100, 8, 92, 0, "idle"),
        ("Петр", "строитель", 100, 12, 88, 3, "idle"),
        ("София", "фермер", 100, 6, 97, 0, "idle"),
        ("Макс", "охотник", 100, 18, 86, 7, "idle"),
    ]
    cursor.executemany(
        """
        INSERT INTO Creature(name, profession, health, hunger, energy, stress, state)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        creatures,
    )

    resources = [
        ("wood", 30),
        ("stone", 20),
        ("food", 35),
        ("energy", 10),
        ("water", 25),
    ]
    cursor.executemany("INSERT INTO ResourceState(type, amount) VALUES (?, ?)", resources)

    buildings = [
        ("Дом", 1, 100, 40, "working", 1, 2),
        ("Ферма", 1, 100, 60, "working", 1, 1),
        ("Склад", 1, 100, 30, "economy_mode", 0.5, 1),
        ("Башня", 1, 85, 20, "damaged", 0, 0),
        ("Мастерская", 2, 90, 75, "upgrading", 2, 0),
    ]
    cursor.executemany(
        """
        INSERT INTO Building(name, level, durability, progress, state, energy_consumption, workers_required)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        buildings,
    )

    tasks = [
        ("build", 3, "new", 1, 1, 0),
        ("farm", 2, "new", 2, 2, 0),
        ("hunt", 2, "new", None, 3, 0),
        ("destroy", 1, "new", 4, 4, 0),
        ("gather_wood", 2, "new", None, 5, 0),
        ("repair", 3, "new", 4, 6, 0),
        ("upgrade", 4, "new", 5, 1, 10),
        ("guard", 1, "new", None, None, 0),
        ("eatfood", 1, "new", None, None, 0),
        ("moveto", 1, "new", None, None, 0),
    ]
    cursor.executemany(
        """
        INSERT INTO Task(type, priority, status, building_id, creature_id, progress)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        tasks,
    )

    cursor.execute(
        "INSERT INTO GameEventLog(event_type, description) VALUES (?, ?)",
        ("init", "База данных создана и заполнена стартовыми данными"),
    )


if __name__ == "__main__":
    path = init_database(reset=True, seed=True)
    print(f"Database initialized and seeded: {path}")
