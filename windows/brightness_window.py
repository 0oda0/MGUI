# windows/brightness_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDial
from PyQt6.QtCore import Qt
from services.brightness_controller import BrightnessController

class BrightnessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Яркость экрана")
        self.setGeometry(200, 200, 300, 300)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.controller = BrightnessController()
        layout = QVBoxLayout(self)

        self.dial = QDial()
        self.dial.setRange(0, 100)
        self.dial.setValue(self.controller.get_brightness())
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.on_brightness_change)
        self.dial.setFixedSize(200, 200)

        self.label = QLabel(f"Яркость: {self.dial.value()}%")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.dial, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addStretch()

    def on_brightness_change(self, value):
        self.controller.set_brightness(value)
        self.label.setText(f"Яркость: {value}%")