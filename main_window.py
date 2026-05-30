# main_window.py (обновлённый)
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget
from PyQt6.QtCore import Qt
from widgets.sidebar import Sidebar
from widgets.work_mode_widget import WorkModeWidget
from widgets.game_mode_widget import GameModeWidget
from config_manager import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MGUI v0.5 — Игровой режим")
        self.setGeometry(100, 100, 900, 600)

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
        self.stack.addWidget(self.work_widget)
        self.stack.addWidget(self.game_widget)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, 1)

        saved_mode = self.config.get("current_mode", "work")
        self.switch_mode(saved_mode)

    def switch_mode(self, mode):
        if mode == "work":
            self.stack.setCurrentIndex(0)
            self.sidebar.set_current_mode("work")
        else:
            self.stack.setCurrentIndex(1)
            self.sidebar.set_current_mode("game")
        self.config.set("current_mode", mode)

    def closeEvent(self, event):
        self.config.set("window_geometry", {
            "x": self.x(), "y": self.y(),
            "width": self.width(), "height": self.height()
        })
        event.ignore()
        self.hide()