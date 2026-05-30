# widgets/work_mode_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from widgets.timer_widget import TimerWidget
from database.db_manager import DatabaseManager

class WorkModeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        self.update_today_stats()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Заголовок
        title = QLabel("Рабочий режим — Таймер продуктивности")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")

        # Виджет таймера
        self.timer_widget = TimerWidget()
        self.timer_widget.session_completed.connect(self.on_session_completed)

        # Статистика за сегодня
        self.stats_label = QLabel("Сегодня отработано: 0 ч 0 мин")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 14px; margin: 10px;")

        # Кнопка сохранения текущей сессии вручную (опционально, но полезно)
        from PyQt6.QtWidgets import QPushButton
        self.save_btn = QPushButton("Завершить сессию и сохранить")
        self.save_btn.clicked.connect(self.save_current_session)

        layout.addWidget(title)
        layout.addWidget(self.timer_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)
        layout.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def on_session_completed(self, seconds: int):
        """Обработчик завершения сессии (автоматически при остановке через виджет)."""
        self.db.add_work_session(seconds)
        self.update_today_stats()

    def save_current_session(self):
        """Вручную завершить текущую сессию и сохранить."""
        self.timer_widget.stop_and_save()

    def update_today_stats(self):
        seconds = self.db.get_today_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        self.stats_label.setText(f"Сегодня отработано: {hours} ч {minutes} мин")