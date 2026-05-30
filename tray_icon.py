from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

class TrayIcon(QSystemTrayIcon):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Создаём иконку программно (16x16, синий квадрат)
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(0, 120, 215))  # Синий цвет
        icon = QIcon(pixmap)
        self.setIcon(icon)

        # Контекстное меню
        self.menu = QMenu()
        show_action = QAction("Показать окно", self)
        show_action.triggered.connect(self.show_window)
        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(self.quit_app)

        self.menu.addAction(show_action)
        self.menu.addAction(quit_action)
        self.menu.addSeparator()
        sound_action = QAction("🔊 Звук", self)
        sound_action.triggered.connect(self.open_sound)
        brightness_action = QAction("🔆 Яркость", self)
        brightness_action.triggered.connect(self.open_brightness)
        apps_action = QAction("🖥️ Окна и приложения", self)
        apps_action.triggered.connect(self.open_apps)
        self.menu.addAction(sound_action)
        self.menu.addAction(brightness_action)
        self.menu.addAction(apps_action)

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_tray_activated)

        self.show()  # Теперь иконка точно есть

    def open_sound(self):
        if hasattr(self.main_window, 'game_mode_widget'):
            self.main_window.game_mode_widget.open_sound_window()

    def open_brightness(self):
        if hasattr(self.main_window, 'game_mode_widget'):
            self.main_window.game_mode_widget.open_brightness_window()

    def open_apps(self):
        if hasattr(self.main_window, 'game_mode_widget'):
            self.main_window.game_mode_widget.open_apps_window()

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