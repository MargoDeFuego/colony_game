import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "colony.db")
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "events.log")


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GameLogger(metaclass=SingletonMeta):
    """Одиночка: один общий лог событий для всей игры."""

    def log(self, event_type, description):
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        message = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {event_type}: {description}"
        print(f"LOG: {description}")
        with open(LOG_PATH, "a", encoding="utf-8") as file:
            file.write(message + "\n")

        if os.path.exists(DB_PATH):
            try:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO GameEventLog(event_type, description) VALUES (?, ?)",
                    (event_type, description),
                )
                conn.commit()
                conn.close()
            except sqlite3.Error:
                # Лог в файл важнее, игра не должна падать из-за ошибки БД.
                pass
