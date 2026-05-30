# widgets/game_mode_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
                             QHBoxLayout, QTabWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from database.game_stats_db import GameStatsDB
from services.game_tracker import GameTracker
from widgets.news_widget import NewsWidget
from widgets.top_processes_widget import TopProcessesWidget
from windows.sound_window import SoundWindow
from windows.brightness_window import BrightnessWindow
from windows.apps_window import AppsWindow
from logger import app_logger

class GameModeWidget(QWidget):
    game_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.db = GameStatsDB()
        self.tracker = GameTracker()
        self.current_game = None

        self.sound_win = None
        self.brightness_win = None
        self.apps_win = None

        self.init_ui()
        self.tracker.game_changed.connect(self.on_game_changed)
        self.tracker.start()

    def init_ui(self):
        layout = QVBoxLayout(self)

        control_btn = QPushButton("⚙️ Центр управления")
        control_btn.clicked.connect(self.open_system_control)
        layout.addWidget(control_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.current_game_label = QLabel("Текущая игра: Не игра")
        self.current_game_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_game_label.setStyleSheet("font-size: 14px; margin: 5px;")

        self.stats_label = QLabel("За последнюю неделю: 0 ч 0 мин")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 12px; margin: 5px;")

        self.tab_widget = QTabWidget()

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Введите заметки по игре...")
        self.notes_edit.textChanged.connect(self.on_notes_changed)
        self.tab_widget.addTab(self.notes_edit, "📝 Заметки")

        self.news_widget = NewsWidget()
        self.tab_widget.addTab(self.news_widget, "📰 Новости")

        self.top_processes = TopProcessesWidget()
        self.tab_widget.addTab(self.top_processes, "⚙️ Система")

        layout.addWidget(self.current_game_label)
        layout.addWidget(self.stats_label)
        layout.addWidget(self.tab_widget)
        layout.addStretch()

    def open_sound_window(self):
        if self.sound_win is None:
            self.sound_win = SoundWindow()
        self.sound_win.show()
        self.sound_win.raise_()

    def open_brightness_window(self):
        if self.brightness_win is None:
            self.brightness_win = BrightnessWindow()
        self.brightness_win.show()
        self.brightness_win.raise_()

    def open_apps_window(self):
        if self.apps_win is None:
            self.apps_win = AppsWindow()
        self.apps_win.show()
        self.apps_win.raise_()

    def open_system_control(self):
        # Ленивый импорт, чтобы избежать ошибок при старте
        from windows.system_control_window import SystemControlWindow
        self.control_win = SystemControlWindow()
        self.control_win.show()

    def on_game_changed(self, game_name: str):
        if self.current_game == game_name:
            return
        if self.current_game:
            self.db.end_current_session()
            self.db.set_note(self.current_game, self.notes_edit.toPlainText())

        self.current_game = game_name
        if game_name:
            self.current_game_label.setText(f"Текущая игра: {game_name}")
            note = self.db.get_note(game_name)
            self.notes_edit.blockSignals(True)
            self.notes_edit.setPlainText(note)
            self.notes_edit.blockSignals(False)
            self.db.start_session(game_name)
            self.refresh_stats()
            self.news_widget.set_game(game_name)
            app_logger.info(f"Обнаружена игра: {game_name}")
        else:
            self.current_game_label.setText("Текущая игра: Не игра")
            self.notes_edit.blockSignals(True)
            self.notes_edit.clear()
            self.notes_edit.blockSignals(False)
            self.stats_label.setText("За последнюю неделю: 0 ч 0 мин")
            self.news_widget.set_game("")
            app_logger.info("Игра не активна")

    def on_notes_changed(self):
        if self.current_game:
            self.db.set_note(self.current_game, self.notes_edit.toPlainText())

    def refresh_stats(self):
        if self.current_game:
            seconds = self.db.get_week_duration(self.current_game)
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            self.stats_label.setText(f"За последнюю неделю: {hours} ч {minutes} мин")
        else:
            self.stats_label.setText("За последнюю неделю: 0 ч 0 мин")