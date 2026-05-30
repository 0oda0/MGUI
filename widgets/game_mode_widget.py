# widgets/game_mode_widget.py (исправленный, полный)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from database.game_stats_db import GameStatsDB
from services.game_tracker import GameTracker

class GameModeWidget(QWidget):
    game_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.db = GameStatsDB()
        self.tracker = GameTracker()
        self.current_game = None

        self.init_ui()
        self.tracker.game_changed.connect(self.on_game_changed)
        self.tracker.start()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Игровой режим — Трекер игр")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")

        self.current_game_label = QLabel("Текущая игра: Не игра")
        self.current_game_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_game_label.setStyleSheet("font-size: 14px; margin: 5px;")

        self.stats_label = QLabel("За последнюю неделю: 0 ч 0 мин")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 12px; margin: 5px;")

        notes_label = QLabel("Заметки по текущей игре:")
        notes_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Введите заметки по игре...")
        self.notes_edit.textChanged.connect(self.on_notes_changed)

        refresh_btn = QPushButton("Обновить статистику")
        refresh_btn.clicked.connect(self.refresh_stats)

        layout.addWidget(title)
        layout.addWidget(self.current_game_label)
        layout.addWidget(self.stats_label)
        layout.addWidget(notes_label)
        layout.addWidget(self.notes_edit)
        layout.addWidget(refresh_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def on_game_changed(self, game_name: str):
        if self.current_game == game_name:
            return
        # Завершаем сессию предыдущей игры
        if self.current_game:
            self.db.end_current_session()
        # Сохраняем заметки предыдущей игры
        if self.current_game:
            self.db.set_note(self.current_game, self.notes_edit.toPlainText())

        self.current_game = game_name
        if game_name:
            self.current_game_label.setText(f"Текущая игра: {game_name}")
            # Загружаем заметки для новой игры
            note = self.db.get_note(game_name)
            self.notes_edit.blockSignals(True)
            self.notes_edit.setPlainText(note)
            self.notes_edit.blockSignals(False)
            # Начинаем сессию новой игры
            self.db.start_session(game_name)
            self.refresh_stats()
        else:
            self.current_game_label.setText("Текущая игра: Не игра")
            self.notes_edit.blockSignals(True)
            self.notes_edit.clear()
            self.notes_edit.blockSignals(False)
            self.stats_label.setText("За последнюю неделю: 0 ч 0 мин")

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

    def closeEvent(self, event):
        # При закрытии виджета не останавливаем трекер, он общий
        event.accept()