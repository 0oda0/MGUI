# tray_icon.py
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QPixmap, QColor

class TrayIcon(QSystemTrayIcon):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(0, 120, 215))
        icon = QIcon(pixmap)
        self.setIcon(icon)

        self.menu = QMenu()
        show_action = QAction("Показать окно", self)
        show_action.triggered.connect(self.show_window)
        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(self.quit_app)

        self.menu.addAction(show_action)
        self.menu.addSeparator()
        work_action = QAction("💼 Работа", self)
        work_action.triggered.connect(lambda: self.switch_mode("work"))
        game_action = QAction("🎮 Игра", self)
        game_action.triggered.connect(lambda: self.switch_mode("game"))
        control_action = QAction("⚙️ Центр управления", self)
        control_action.triggered.connect(lambda: self.switch_mode("control"))
        self.menu.addAction(work_action)
        self.menu.addAction(game_action)
        self.menu.addAction(control_action)
        self.menu.addSeparator()
        self.menu.addAction(quit_action)

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_tray_activated)
        self.show()

    def switch_mode(self, mode):
        self.main_window.switch_mode(mode)
        self.show_window()

    def show_window(self):
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def quit_app(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()