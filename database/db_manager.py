# database/db_manager.py
import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="mgui.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS work_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    month INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    seconds INTEGER NOT NULL
                )
            """)
            conn.commit()

    def add_work_session(self, seconds: int):
        """Добавляет рабочую сессию (секунды) с текущей датой."""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        month = now.month
        year = now.year
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO work_sessions (date, month, year, seconds) VALUES (?, ?, ?, ?)",
                (date_str, month, year, seconds)
            )
            conn.commit()

    def get_today_seconds(self) -> int:
        """Возвращает общее количество секунд, отработанных сегодня."""
        today = datetime.now().strftime("%Y-%m-%d")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT SUM(seconds) FROM work_sessions WHERE date = ?",
                (today,)
            )
            result = cursor.fetchone()[0]
            return result if result is not None else 0