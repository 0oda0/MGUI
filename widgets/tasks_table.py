# widgets/tasks_table.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QAbstractItemView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from database.tasks_db import TasksDB

class TasksTable(QWidget):
    task_changed = pyqtSignal()  # сигнал для обновления внешней статистики при изменении

    def __init__(self):
        super().__init__()
        self.db = TasksDB()
        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Добавить")
        self.edit_btn = QPushButton("✏️ Редактировать")
        self.delete_btn = QPushButton("🗑 Удалить")
        self.refresh_btn = QPushButton("🔄 Обновить")

        self.add_btn.clicked.connect(self.add_task)
        self.edit_btn.clicked.connect(self.edit_task)
        self.delete_btn.clicked.connect(self.delete_task)
        self.refresh_btn.clicked.connect(self.load_tasks)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Важная", "Срочная", "Выполнено"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemClicked.connect(self.on_item_clicked)  # для обработки клика по галочке

        layout.addLayout(btn_layout)
        layout.addWidget(self.table)

    def load_tasks(self):
        tasks = self.db.get_all_tasks()
        # Сортировка: сначала невыполненные (completed = False), среди них urgent=True выше,
        # затем выполненные внизу
        def sort_key(t):
            # (completed, -urgent, -important, title)
            return (t["completed"], not t["urgent"], not t["important"], t["title"])
        tasks.sort(key=sort_key)

        self.table.setRowCount(len(tasks))
        self.task_rows = {}  # mapping row -> task_id

        for row, task in enumerate(tasks):
            self.task_rows[row] = task["id"]

            # Название
            title_item = QTableWidgetItem(task["title"])
            if task["completed"]:
                font = QFont()
                font.setStrikeOut(True)
                title_item.setFont(font)
                title_item.setForeground(Qt.GlobalColor.gray)
            self.table.setItem(row, 0, title_item)

            # Важная (галочка текстом)
            important_item = QTableWidgetItem("✅" if task["important"] else "❌")
            important_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, important_item)

            # Срочная
            urgent_item = QTableWidgetItem("⚠️" if task["urgent"] else "❌")
            urgent_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, urgent_item)

            # Выполнено — чекбокс в ячейке? Проще текстом с галочкой, но можно и QCheckBox, но сложнее.
            # Используем кликабельный текст: ☐ / ☑
            completed_text = "☑" if task["completed"] else "☐"
            completed_item = QTableWidgetItem(completed_text)
            completed_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, completed_item)

            # Подсветка срочных задач (красный фон) — если urgent и не выполнена
            if task["urgent"] and not task["completed"]:
                for col in range(4):
                    self.table.item(row, col).setBackground(Qt.GlobalColor.red)
                    self.table.item(row, col).setForeground(Qt.GlobalColor.white)
            else:
                # Сброс цвета для остальных (но может быть уже окрашено)
                for col in range(4):
                    self.table.item(row, col).setBackground(Qt.GlobalColor.transparent)
                    if not task["completed"]:
                        self.table.item(row, col).setForeground(Qt.GlobalColor.black)
                    else:
                        self.table.item(row, col).setForeground(Qt.GlobalColor.gray)

        self.table.resizeColumnsToContents()
        self.task_changed.emit()

    def on_item_clicked(self, item):
        # Если клик по колонке "Выполнено" (индекс 3)
        if item.column() == 3:
            row = item.row()
            task_id = self.task_rows.get(row)
            if task_id is not None:
                self.db.toggle_completed(task_id)
                self.load_tasks()

    def get_current_task_id(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            return self.task_rows.get(current_row)
        return None

    def add_task(self):
        from dialogs.task_edit_dialog import TaskEditDialog
        dlg = TaskEditDialog()
        if dlg.exec():
            data = dlg.get_data()
            if data["title"].strip():
                self.db.add_task(data["title"], data["important"], data["urgent"])
                self.load_tasks()

    def edit_task(self):
        task_id = self.get_current_task_id()
        if task_id is None:
            return
        tasks = self.db.get_all_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task:
            from dialogs.task_edit_dialog import TaskEditDialog
            dlg = TaskEditDialog(task["title"], task["important"], task["urgent"])
            if dlg.exec():
                data = dlg.get_data()
                if data["title"].strip():
                    self.db.update_task(task_id, data["title"], data["important"], data["urgent"], task["completed"])
                    self.load_tasks()

    def delete_task(self):
        task_id = self.get_current_task_id()
        if task_id is None:
            return
        self.db.delete_task(task_id)
        self.load_tasks()