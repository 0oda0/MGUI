# widgets/game_mode_widget.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class GameModeWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Игровой режим\n(здесь будет трекер игр, громкость, яркость)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)