# widgets/pinned_apps_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from services.pinned_apps_manager import PinnedAppsManager
from dialogs.app_picker_dialog import AppPickerDialog
import os
from logger import app_logger

class PinnedAppsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = PinnedAppsManager()
        self.init_ui()
        self.refresh_list()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self.launch_app)
        self.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.show_context_menu)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕")
        add_btn.setFixedSize(30, 30)
        add_btn.setToolTip("Добавить приложение")
        add_btn.clicked.connect(self.add_app)
        remove_btn = QPushButton("❌")
        remove_btn.setFixedSize(30, 30)
        remove_btn.setToolTip("Удалить выбранное")
        remove_btn.clicked.connect(self.remove_app)

        btn_layout.addStretch()
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addStretch()

        layout.addWidget(self.list)
        layout.addLayout(btn_layout)

    def refresh_list(self):
        self.list.clear()
        for app in self.manager.get_all():
            item = QListWidgetItem(app["name"])
            item.setData(Qt.ItemDataRole.UserRole, app["path"])
            self.list.addItem(item)

    def launch_app(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        try:
            os.startfile(path)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось запустить:\n{e}")

    def add_app(self):
        dlg = AppPickerDialog()
        if dlg.exec():
            name, path = dlg.get_selected_app()
            if path:
                self.manager.add(name, path)
                self.refresh_list()
                app_logger.info(f"Закреплено приложение: {name} ({path})")

    def remove_app(self):
        item = self.list.currentItem()
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            self.manager.remove(path)
            self.refresh_list()
        app_logger.info(f"Удалено из закреплённых: {path}")

    def show_context_menu(self, pos):
        item = self.list.itemAt(pos)
        if item:
            menu = self.list.createStandardContextMenu()
            menu.exec(self.list.viewport().mapToGlobal(pos))