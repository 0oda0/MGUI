# database/game_stats_db.py
import sqlite3
from datetime import datetime, timedelta

class GameStatsDB:
    def __init__(self, db_path="mgui.db"):
        self.db_path = db_path
        self._init_tables()

    def _init_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_name TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    duration_seconds INTEGER NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_notes (
                    game_name TEXT PRIMARY KEY,
                    notes TEXT NOT NULL
                )
            """)
            conn.commit()

    def start_session(self, game_name: str):
        """Начинаем новую сессию для игры (если уже есть незавершённая — завершить её)."""
        self.end_current_session()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO game_sessions (game_name, start_time, end_time, duration_seconds) VALUES (?, ?, ?, ?)",
                (game_name, datetime.now().isoformat(), "", 0)
            )
            conn.commit()
            return cursor.lastrowid

    def end_current_session(self):
        """Завершает текущую активную сессию (ту, у которой end_time = '' или NULL)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, start_time FROM game_sessions WHERE end_time = '' OR end_time IS NULL ORDER BY start_time DESC LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                session_id, start_str = row
                start_time = datetime.fromisoformat(start_str)
                end_time = datetime.now()
                duration = int((end_time - start_time).total_seconds())
                cursor.execute(
                    "UPDATE game_sessions SET end_time = ?, duration_seconds = ? WHERE id = ?",
                    (end_time.isoformat(), duration, session_id)
                )
                conn.commit()

    def get_week_duration(self, game_name: str) -> int:
        """Возвращает общее количество секунд, сыгранных в игру за последние 7 дней."""
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT SUM(duration_seconds) FROM game_sessions WHERE game_name = ? AND start_time >= ?",
                (game_name, week_ago)
            )
            result = cursor.fetchone()[0]
            return result if result is not None else 0

    def get_note(self, game_name: str) -> str:
        """Получить заметку для игры."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT notes FROM game_notes WHERE game_name = ?", (game_name,))
            row = cursor.fetchone()
            return row[0] if row else ""

    def set_note(self, game_name: str, note: str):
        """Сохранить заметку для игры (upsert)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO game_notes (game_name, notes) VALUES (?, ?)",
                (game_name, note)
            )
            conn.commit()