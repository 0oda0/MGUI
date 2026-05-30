# widgets/control_center_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QFrame)
from PyQt6.QtCore import Qt
from logger import app_logger

class ControlCenterWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Инициализация контроллеров с защитой
        self.audio = None
        self.brightness = None
        try:
            from services.audio_controller import AudioController
            self.audio = AudioController()
            app_logger.info("Аудиоконтроллер инициализирован")
        except Exception as e:
            app_logger.error(f"Ошибка инициализации аудио: {e}")
        try:
            from services.brightness_controller import BrightnessController
            self.brightness = BrightnessController()
            app_logger.info("Контроллер яркости инициализирован")
        except Exception as e:
            app_logger.error(f"Ошибка инициализации яркости: {e}")

        self.init_ui()
        self.load_audio_devices()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Громкость системы ---
        vol_group = self._create_group("🔊 Громкость системы")
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        if self.audio:
            try:
                self.vol_slider.setValue(self.audio.get_system_volume())
                self.vol_slider.valueChanged.connect(self.on_volume_change)
            except Exception as e:
                app_logger.error(f"Ошибка настройки ползунка громкости: {e}")
                self.vol_slider.setEnabled(False)
        else:
            self.vol_slider.setEnabled(False)
        self.vol_slider.setValue(50)  # значение по умолчанию
        self.vol_value = QLabel(f"{self.vol_slider.value()}%")
        self.vol_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vol_group.layout().addWidget(self.vol_slider)
        vol_group.layout().addWidget(self.vol_value)
        layout.addWidget(vol_group)

        # --- Громкость микрофона (заглушка) ---
        mic_group = self._create_group("🎤 Громкость микрофона")
        self.mic_slider = QSlider(Qt.Orientation.Horizontal)
        self.mic_slider.setRange(0, 100)
        self.mic_slider.setValue(50)
        self.mic_slider.setEnabled(False)
        self.mic_value = QLabel("50% (не поддерживается)")
        self.mic_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mic_group.layout().addWidget(self.mic_slider)
        mic_group.layout().addWidget(self.mic_value)
        layout.addWidget(mic_group)

        # --- Яркость экрана ---
        bright_group = self._create_group("☀️ Яркость экрана")
        self.bright_slider = QSlider(Qt.Orientation.Horizontal)
        self.bright_slider.setRange(0, 100)
        if self.brightness:
            try:
                self.bright_slider.setValue(self.brightness.get_brightness())
                self.bright_slider.valueChanged.connect(self.on_brightness_change)
            except Exception as e:
                app_logger.error(f"Ошибка настройки ползунка яркости: {e}")
                self.bright_slider.setEnabled(False)
        else:
            self.bright_slider.setEnabled(False)
        self.bright_slider.setValue(50)
        self.bright_value = QLabel(f"{self.bright_slider.value()}%")
        self.bright_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bright_group.layout().addWidget(self.bright_slider)
        bright_group.layout().addWidget(self.bright_value)
        layout.addWidget(bright_group)

        # --- Выбор аудиоустройства ---
        device_group = self._create_group("🎧 Основное аудиоустройство")
        self.device_combo = QComboBox()
        self.device_combo.currentTextChanged.connect(self.on_device_changed)
        device_group.layout().addWidget(self.device_combo)
        layout.addWidget(device_group)

        # --- Закреплённые приложения ---
        pinned_group = self._create_group("📌 Закреплённые программы")
        from widgets.pinned_apps_widget import PinnedAppsWidget
        self.pinned_widget = PinnedAppsWidget()
        pinned_group.layout().addWidget(self.pinned_widget)
        layout.addWidget(pinned_group)

        layout.addStretch()

    def _create_group(self, title):
        """Создаёт группу (рамку с заголовком и вертикальным layout)."""
        frame = QFrame()
        frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px; padding: 10px;")
        layout = QVBoxLayout(frame)   # layout автоматически привязывается к frame
        label = QLabel(title)
        label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(label)
        return frame

    def load_audio_devices(self):
        try:
            from pycaw.pycaw import AudioUtilities
            devices = AudioUtilities.GetAllDevices()
            names = [dev.FriendlyName for dev in devices if dev.FriendlyName]
            if not names:
                names = ["Устройство по умолчанию"]
            self.device_combo.addItems(names)
            app_logger.info(f"Загружено аудиоустройств: {len(names)}")
        except Exception as e:
            app_logger.error(f"Ошибка загрузки устройств: {e}")
            self.device_combo.addItem("Устройство по умолчанию")

    def on_volume_change(self, value):
        if self.audio:
            try:
                self.audio.set_system_volume(value)
                self.vol_value.setText(f"{value}%")
                app_logger.info(f"Громкость изменена: {value}%")
            except Exception as e:
                app_logger.error(f"Ошибка установки громкости: {e}")

    def on_brightness_change(self, value):
        if self.brightness:
            try:
                self.brightness.set_brightness(value)
                self.bright_value.setText(f"{value}%")
                app_logger.info(f"Яркость изменена: {value}%")
            except Exception as e:
                app_logger.error(f"Ошибка установки яркости: {e}")

    def on_device_changed(self, device_name):
        app_logger.info(f"Выбрано устройство: {device_name}")