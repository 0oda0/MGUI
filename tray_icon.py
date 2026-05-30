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

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_tray_activated)

        self.show()  # Теперь иконка точно есть

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