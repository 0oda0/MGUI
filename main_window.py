from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MGUI - Минимальный каркас")
        self.setGeometry(100, 100, 800, 600)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        label = QLabel("MGUI v0.1\nПриложение запущено от имени администратора.\nЗакрытие окна сворачивает в трей.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

    def closeEvent(self, event):
        """Переопределяем закрытие окна: скрываем окно, а не закрываем приложение."""
        event.ignore()
        self.hide()