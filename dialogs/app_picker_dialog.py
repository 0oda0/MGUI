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

        label = QLabel("Выберите .exe файл:")
        layout.addWidget(label)

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

    def browse_exe(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать исполняемый файл", "", "Executable files (*.exe);;All files (*.*)")
        if path:
            self.selected_name = os.path.basename(path)
            self.selected_path = path
            self.accept()

    def get_selected_app(self):
        return self.selected_name, self.selected_path