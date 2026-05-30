# dialogs/app_picker_dialog.py
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QListWidget, QPushButton,
                             QFileDialog, QHBoxLayout, QLabel)
import os

class AppPickerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбрать приложение")
        self.setModal(True)
        self.selected_name = ""
        self.selected_path = ""

        layout = QVBoxLayout(self)

        label = QLabel("Выберите приложение из списка или укажите вручную:")
        layout.addWidget(label)

        self.list = QListWidget()
        self.populate_common_apps()
        layout.addWidget(self.list)

        btn_layout = QHBoxLayout()
        browse_btn = QPushButton("Обзор...")
        browse_btn.clicked.connect(self.browse_exe)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(browse_btn)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.list.itemDoubleClicked.connect(self.on_item_double_click)

    def populate_common_apps(self):
        # Пример: поиск ярлыков в меню Пуск
        start_menu = os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs")
        if os.path.exists(start_menu):
            for root, dirs, files in os.walk(start_menu):
                for file in files:
                    if file.endswith(".lnk"):
                        self.list.addItem(file[:-4])
        # Также можно добавить популярные пути
        common_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)"
        ]
        # Упрощённо: не парсим все, пользователь может сам выбрать через обзор

    def browse_exe(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать исполняемый файл", "", "Executable files (*.exe);;All files (*.*)")
        if path:
            self.selected_name = os.path.basename(path)
            self.selected_path = path
            self.accept()

    def on_item_double_click(self, item):
        # Здесь нужно найти путь к программе по имени ярлыка, но сложно.
        # Для простоты предложим пользователю выбрать через обзор.
        pass

    def get_selected_app(self):
        return self.selected_name, self.selected_path