# windows/sound_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt6.QtCore import Qt
from services.audio_controller import AudioController

class SoundWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление звуком")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.audio = AudioController()

        layout = QVBoxLayout(self)

        # Системная громкость
        sys_layout = QHBoxLayout()
        sys_label = QLabel("Громкость системы:")
        self.sys_slider = QSlider(Qt.Orientation.Horizontal)
        self.sys_slider.setRange(0, 100)
        self.sys_slider.setValue(int(self.audio.get_system_volume()))
        self.sys_slider.valueChanged.connect(self.on_sys_volume)
        self.sys_val_label = QLabel(f"{int(self.audio.get_system_volume())}%")
        sys_layout.addWidget(sys_label)
        sys_layout.addWidget(self.sys_slider)
        sys_layout.addWidget(self.sys_val_label)
        layout.addLayout(sys_layout)

        # Громкость микрофона (заглушка)
        mic_layout = QHBoxLayout()
        mic_label = QLabel("Громкость микрофона:")
        self.mic_slider = QSlider(Qt.Orientation.Horizontal)
        self.mic_slider.setRange(0, 100)
        self.mic_slider.setValue(50)
        self.mic_slider.setEnabled(False)  # пока не реализовано
        self.mic_val_label = QLabel("50%")
        mic_layout.addWidget(mic_label)
        mic_layout.addWidget(self.mic_slider)
        mic_layout.addWidget(self.mic_val_label)
        layout.addLayout(mic_layout)

        layout.addStretch()

    def on_sys_volume(self, value):
        self.audio.set_system_volume(value)
        self.sys_val_label.setText(f"{value}%")