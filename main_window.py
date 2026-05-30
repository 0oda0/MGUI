# main_window.py
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget
from PyQt6.QtCore import Qt
from widgets.sidebar import Sidebar
from widgets.work_mode_widget import WorkModeWidget
from widgets.game_mode_widget import GameModeWidget
from widgets.control_center_widget import ControlCenterWidget
from widgets.quick_panel import QuickPanel
from config_manager import ConfigManager
from logger import app_logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MGUI v0.9 — Центр управления")
        self.setGeometry(100, 100, 1200, 700)

        self.config = ConfigManager()

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.mode_changed.connect(self.switch_mode)

        self.stack = QStackedWidget()
        self.work_widget = WorkModeWidget()
        self.game_widget = GameModeWidget()
        self.control_widget = ControlCenterWidget()   # обязательно

        self.stack.addWidget(self.work_widget)    # index 0
        self.stack.addWidget(self.game_widget)    # index 1
        self.stack.addWidget(self.control_widget) # index 2

        self.game_mode_widget = self.game_widget

        self.quick_panel = QuickPanel()

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, 1)
        main_layout.addWidget(self.quick_panel)

        saved_mode = self.config.get("current_mode", "work")
        self.switch_mode(saved_mode)

    def switch_mode(self, mode):
        if mode == "work":
            self.stack.setCurrentIndex(0)
            self.sidebar.set_current_mode("work")
            app_logger.info("Переключение в режим 'Работа'")
        elif mode == "game":
            self.stack.setCurrentIndex(1)
            self.sidebar.set_current_mode("game")
            app_logger.info("Переключение в режим 'Игра'")
        elif mode == "control":
            self.stack.setCurrentIndex(2)
            self.sidebar.set_current_mode("control")
            app_logger.info("Переключение в режим 'Центр управления'")
        else:
            return
        self.config.set("current_mode", mode)

    def closeEvent(self, event):
        self.config.set("window_geometry", {
            "x": self.x(), "y": self.y(),
            "width": self.width(), "height": self.height()
        })
        app_logger.info("Окно скрыто в трей")
        event.ignore()
        self.hide()