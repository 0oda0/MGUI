# widgets/work_mode_widget.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class WorkModeWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Рабочий режим\n(здесь будет таймер и задачи)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)