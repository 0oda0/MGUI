# windows/apps_window.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                             QPushButton, QHBoxLayout, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
import win32gui
import win32con
import psutil
import os
from dialogs.app_picker_dialog import AppPickerDialog

class AppsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окна и приложения")
        self.setGeometry(200, 200, 500, 500)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.pinned_apps = self.load_pinned_apps()

        layout = QVBoxLayout(self)

        # Блок открытых окон
        windows_label = QLabel("Открытые окна:")
        windows_label.setStyleSheet("font-weight: bold;")
        self.windows_list = QListWidget()
        self.windows_list.itemDoubleClicked.connect(self.activate_window)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.refresh_windows)
        close_btn = QPushButton("Закрыть выбранное окно")
        close_btn.clicked.connect(self.close_selected_window)

        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(close_btn)

        # Блок закреплённых приложений
        pinned_label = QLabel("Закреплённые приложения:")
        pinned_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        self.pinned_list = QListWidget()
        self.pinned_list.itemDoubleClicked.connect(self.launch_pinned)

        pinned_btn_layout = QHBoxLayout()
        add_pinned_btn = QPushButton("➕ Добавить приложение")
        add_pinned_btn.clicked.connect(self.add_pinned_app)
        remove_pinned_btn = QPushButton("🗑 Удалить выбранное")
        remove_pinned_btn.clicked.connect(self.remove_pinned_app)

        pinned_btn_layout.addWidget(add_pinned_btn)
        pinned_btn_layout.addWidget(remove_pinned_btn)

        layout.addWidget(windows_label)
        layout.addWidget(self.windows_list)
        layout.addLayout(btn_layout)
        layout.addWidget(pinned_label)
        layout.addWidget(self.pinned_list)
        layout.addLayout(pinned_btn_layout)

        self.refresh_windows()
        self.refresh_pinned_list()

    def refresh_windows(self):
        self.windows_list.clear()
        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                windows.append((hwnd, win32gui.GetWindowText(hwnd)))
            return True
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        for hwnd, title in windows:
            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, hwnd)
            self.windows_list.addItem(item)

    def activate_window(self, item):
        hwnd = item.data(Qt.ItemDataRole.UserRole)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

    def close_selected_window(self):
        item = self.windows_list.currentItem()
        if item:
            hwnd = item.data(Qt.ItemDataRole.UserRole)
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def load_pinned_apps(self):
        # Загружаем из конфига или из файла
        import json
        if os.path.exists("pinned_apps.json"):
            with open("pinned_apps.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_pinned_apps(self):
        import json
        with open("pinned_apps.json", "w", encoding="utf-8") as f:
            json.dump(self.pinned_apps, f, indent=2)

    def refresh_pinned_list(self):
        self.pinned_list.clear()
        for app in self.pinned_apps:
            item = QListWidgetItem(f"{app['name']} ({app['path']})")
            item.setData(Qt.ItemDataRole.UserRole, app['path'])
            self.pinned_list.addItem(item)

    def add_pinned_app(self):
        dlg = AppPickerDialog()
        if dlg.exec():
            name, path = dlg.get_selected_app()
            if path:
                self.pinned_apps.append({"name": name, "path": path})
                self.save_pinned_apps()
                self.refresh_pinned_list()

    def remove_pinned_app(self):
        item = self.pinned_list.currentItem()
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            self.pinned_apps = [app for app in self.pinned_apps if app['path'] != path]
            self.save_pinned_apps()
            self.refresh_pinned_list()

    def launch_pinned(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        try:
            os.startfile(path)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось запустить: {e}")