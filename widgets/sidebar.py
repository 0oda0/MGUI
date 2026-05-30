# widgets/sidebar.py (добавлен пункт "Центр управления")
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

class Sidebar(QWidget):
    mode_changed = pyqtSignal(str)  # сигнал: "work" / "game" / "control"

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(150)
        self.list_widget.setFont(QFont("Segoe UI", 10))

        work_item = QListWidgetItem("💼 Работа")
        game_item = QListWidgetItem("🎮 Игра")
        control_item = QListWidgetItem("⚙️ Центр управления")

        self.list_widget.addItem(work_item)
        self.list_widget.addItem(game_item)
        self.list_widget.addItem(control_item)

        self.list_widget.setCurrentRow(0)
        self.list_widget.currentRowChanged.connect(self.on_row_changed)

        layout.addWidget(self.list_widget)
        layout.addStretch()

    def on_row_changed(self, row):
        if row == 0:
            mode = "work"
        elif row == 1:
            mode = "game"
        else:
            mode = "control"
        self.mode_changed.emit(mode)

    def set_current_mode(self, mode):
        if mode == "work":
            self.list_widget.setCurrentRow(0)
        elif mode == "game":
            self.list_widget.setCurrentRow(1)
        else:
            self.list_widget.setCurrentRow(2)