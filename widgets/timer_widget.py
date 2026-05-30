# widgets/timer_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from logger import app_logger

class TimerWidget(QWidget):
    session_completed = pyqtSignal(int)  # излучается при остановке таймера, передаёт секунды

    def __init__(self):
        super().__init__()
        self.elapsed_seconds = 0  # секунды текущей сессии
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Круговой прогресс бар (стилизуем в круг)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # пока без лимита, будет показывать "занято"
        self.progress.setFormat("%v с")  # показываем секунды
        self.progress.setFixedSize(200, 200)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)

        # Стиль для круглого прогресс-бара (через QSS)
        self.progress.setStyleSheet("""
            QProgressBar {
                border-radius: 100px;
                background-color: #2d2d2d;
                text-align: center;
                font: bold 16px;
                color: white;
            }
            QProgressBar::chunk {
                border-radius: 100px;
                background-color: #4caf50;
            }
        """)

        # Отображение времени текстом
        self.time_label = QLabel("00:00:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))

        # Кнопки
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Старт")
        self.pause_btn = QPushButton("Пауза")
        self.reset_btn = QPushButton("Сброс")

        self.start_btn.clicked.connect(self.start)
        self.pause_btn.clicked.connect(self.pause)
        self.reset_btn.clicked.connect(self.reset)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.reset_btn)

        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)
        layout.addLayout(btn_layout)

        self.update_buttons()

    def _update_time(self):
        if self.running:
            self.elapsed_seconds += 1
            self._refresh_display()

    def _refresh_display(self):
        # Обновляем текстовое отображение
        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60
        self.time_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        # Обновляем прогресс-бар (если нужно, но сейчас он круговой и без лимита)
        self.progress.setValue(self.elapsed_seconds)
        self.progress.setFormat(f"{self.elapsed_seconds} с")

    def start(self):
        if not self.running:
            self.running = True
            self.timer.start(1000)
            self.update_buttons()
            app_logger.info("Таймер запущен")

    def pause(self):
        if self.running:
            self.running = False
            self.timer.stop()
            self.update_buttons()
            app_logger.info("Таймер на паузе")

    def reset(self):
        self.running = False
        self.timer.stop()
        # Если была сессия с ненулевым временем, не сбрасываем автоматически — по желанию
        # Согласно логике: при сбросе обнуляем и не сохраняем
        self.elapsed_seconds = 0
        self._refresh_display()
        self.update_buttons()

    def stop_and_save(self):
        """Останавливает и излучает сигнал с отработанными секундами (если >0)."""
        if self.elapsed_seconds > 0:
            seconds = self.elapsed_seconds
            self.reset()  # обнуляет и останавливает
            self.session_completed.emit(seconds)
        else:
            self.reset()

    def update_buttons(self):
        self.start_btn.setEnabled(not self.running)
        self.pause_btn.setEnabled(self.running)
        self.reset_btn.setEnabled(True)