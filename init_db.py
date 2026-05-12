import sqlite3

conn = sqlite3.connect("colony.db")
cursor = conn.cursor()

# Таблица поселенцев
cursor.execute("""
CREATE TABLE IF NOT EXISTS Creature (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    profession TEXT,
    health INTEGER,
    hunger INTEGER,
    energy INTEGER,
    state TEXT
);
""")

# Таблица ресурсов
cursor.execute("""
CREATE TABLE IF NOT EXISTS ResourceState (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount INTEGER
);
""")

# Таблица зданий
cursor.execute("""
CREATE TABLE IF NOT EXISTS Building (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    level INTEGER,
    durability INTEGER
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    priority INTEGER,
    status TEXT
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS GameEventLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()
print("Database initialized.")
