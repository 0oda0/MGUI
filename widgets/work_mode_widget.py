# widgets/work_mode_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSplitter
from PyQt6.QtCore import Qt
from widgets.timer_widget import TimerWidget
from widgets.tasks_table import TasksTable
from database.db_manager import DatabaseManager
from logger import app_logger  # ДОБАВЛЕН ИМПОРТ

class WorkModeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.timer_widget = TimerWidget()
        self.tasks_table = TasksTable()
        self.stats_label = QLabel("Сегодня отработано: 0 ч 0 мин")
        self.save_btn = QPushButton("Завершить сессию и сохранить")
        self.init_ui()
        self.update_today_stats()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        title = QLabel("Рабочий режим — Таймер + Задачи")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")

        splitter = QSplitter(Qt.Orientation.Vertical)

        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        self.timer_widget.session_completed.connect(self.on_session_completed)

        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 14px; margin: 10px;")

        self.save_btn.clicked.connect(self.save_current_session)

        top_layout.addWidget(self.timer_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.stats_label)
        top_layout.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        tasks_label = QLabel("Мои задачи")
        tasks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tasks_label.setStyleSheet("font-weight: bold;")
        self.tasks_table.task_changed.connect(self.on_tasks_changed)
        bottom_layout.addWidget(tasks_label)
        bottom_layout.addWidget(self.tasks_table)

        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)
        splitter.setSizes([300, 300])

        main_layout.addWidget(title)
        main_layout.addWidget(splitter)

    def on_session_completed(self, seconds: int):
        self.db.add_work_session(seconds)
        self.update_today_stats()
        app_logger.info(f"Рабочая сессия сохранена: {seconds} сек.")

    def save_current_session(self):
        self.timer_widget.stop_and_save()
        app_logger.info("Рабочая сессия завершена вручную")

    def update_today_stats(self):
        seconds = self.db.get_today_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        self.stats_label.setText(f"Сегодня отработано: {hours} ч {minutes} мин")

    def on_tasks_changed(self):
        pass