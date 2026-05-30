# database/tasks_db.py
import sqlite3

class TasksDB:
    def __init__(self, db_path="mgui.db"):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    important INTEGER NOT NULL DEFAULT 0,
                    urgent INTEGER NOT NULL DEFAULT 0,
                    completed INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.commit()

    def get_all_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, important, urgent, completed FROM tasks")
            rows = cursor.fetchall()
            return [{
                "id": row[0],
                "title": row[1],
                "important": bool(row[2]),
                "urgent": bool(row[3]),
                "completed": bool(row[4])
            } for row in rows]

    def add_task(self, title: str, important: bool, urgent: bool):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, important, urgent, completed) VALUES (?, ?, ?, 0)",
                (title, int(important), int(urgent))
            )
            conn.commit()
            return cursor.lastrowid

    def update_task(self, task_id: int, title: str, important: bool, urgent: bool, completed: bool):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET title=?, important=?, urgent=?, completed=? WHERE id=?",
                (title, int(important), int(urgent), int(completed), task_id)
            )
            conn.commit()

    def delete_task(self, task_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()

    def toggle_completed(self, task_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET completed = NOT completed WHERE id=?", (task_id,))
            conn.commit()