# windows/system_control_window.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSlider, QComboBox, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from services.audio_controller import AudioController
from services.brightness_controller import BrightnessController
from widgets.pinned_apps_widget import PinnedAppsWidget
from pycaw.pycaw import AudioUtilities

class SystemControlWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Центр управления")
        self.setGeometry(200, 200, 450, 550)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.audio = AudioController()
        self.brightness = BrightnessController()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # --- Громкость ---
        vol_frame = QFrame()
        vol_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        vol_layout = QVBoxLayout(vol_frame)
        vol_label = QLabel("🔊 Громкость системы")
        vol_label.setStyleSheet("font-weight: bold;")
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(self.audio.get_system_volume())
        self.vol_slider.valueChanged.connect(self.on_volume_change)
        self.vol_value = QLabel(f"{self.vol_slider.value()}%")
        vol_layout.addWidget(vol_label)
        vol_layout.addWidget(self.vol_slider)
        vol_layout.addWidget(self.vol_value, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(vol_frame)

        # --- Микрофон (заглушка, но можно реализовать) ---
        mic_frame = QFrame()
        mic_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        mic_layout = QVBoxLayout(mic_frame)
        mic_label = QLabel("🎤 Громкость микрофона")
        mic_label.setStyleSheet("font-weight: bold;")
        self.mic_slider = QSlider(Qt.Orientation.Horizontal)
        self.mic_slider.setRange(0, 100)
        self.mic_slider.setValue(50)
        self.mic_slider.setEnabled(False)  # требует реализации
        self.mic_value = QLabel("50%")
        mic_layout.addWidget(mic_label)
        mic_layout.addWidget(self.mic_slider)
        mic_layout.addWidget(self.mic_value, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mic_frame)

        # --- Яркость ---
        bright_frame = QFrame()
        bright_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        bright_layout = QVBoxLayout(bright_frame)
        bright_label = QLabel("☀️ Яркость экрана")
        bright_label.setStyleSheet("font-weight: bold;")
        self.bright_slider = QSlider(Qt.Orientation.Horizontal)
        self.bright_slider.setRange(0, 100)
        self.bright_slider.setValue(self.brightness.get_brightness())
        self.bright_slider.valueChanged.connect(self.on_brightness_change)
        self.bright_value = QLabel(f"{self.bright_slider.value()}%")
        bright_layout.addWidget(bright_label)
        bright_layout.addWidget(self.bright_slider)
        bright_layout.addWidget(self.bright_value, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(bright_frame)

        # --- Выбор аудиоустройства ---
        device_frame = QFrame()
        device_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        device_layout = QVBoxLayout(device_frame)
        device_label = QLabel("🎧 Основное аудиоустройство")
        device_label.setStyleSheet("font-weight: bold;")
        self.device_combo = QComboBox()
        self.device_combo.addItems(self.get_audio_devices())
        device_layout.addWidget(device_label)
        device_layout.addWidget(self.device_combo)
        layout.addWidget(device_frame)

        # --- Закреплённые приложения (компактная версия) ---
        pinned_frame = QFrame()
        pinned_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        pinned_layout = QVBoxLayout(pinned_frame)
        pinned_label = QLabel("📌 Закреплённые программы")
        pinned_label.setStyleSheet("font-weight: bold;")
        self.pinned_widget = PinnedAppsWidget()
        pinned_layout.addWidget(pinned_label)
        pinned_layout.addWidget(self.pinned_widget)
        layout.addWidget(pinned_frame)

        layout.addStretch()

    def on_volume_change(self, value):
        self.audio.set_system_volume(value)
        self.vol_value.setText(f"{value}%")

    def on_brightness_change(self, value):
        self.brightness.set_brightness(value)
        self.bright_value.setText(f"{value}%")

    def get_audio_devices(self):
        devices = AudioUtilities.GetAllDevices()
        names = []
        for dev in devices:
            if dev.Activate:
                names.append(dev.FriendlyName)
        return names if names else ["Устройство по умолчанию"]