# widgets/sidebar.py
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

class Sidebar(QWidget):
    mode_changed = pyqtSignal(str)  # сигнал: "work" или "game"

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(150)
        self.list_widget.setFont(QFont("Segoe UI", 10))

        # Добавляем пункты
        work_item = QListWidgetItem("💼 Работа")
        game_item = QListWidgetItem("🎮 Игра")

        self.list_widget.addItem(work_item)
        self.list_widget.addItem(game_item)

        # Выделяем первый по умолчанию
        self.list_widget.setCurrentRow(0)

        # Подключаем сигнал
        self.list_widget.currentRowChanged.connect(self.on_row_changed)

        layout.addWidget(self.list_widget)
        layout.addStretch()

    def on_row_changed(self, row):
        mode = "work" if row == 0 else "game"
        self.mode_changed.emit(mode)

    def set_current_mode(self, mode):
        row = 0 if mode == "work" else 1
        self.list_widget.setCurrentRow(row)