import sys
import os
import ctypes
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from tray_icon import TrayIcon

def is_admin():
    """Проверка, запущено ли приложение от имени администратора."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Перезапуск текущего скрипта с правами администратора."""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

def main():
    """Точка входа в приложение."""
    if not is_admin():
        run_as_admin()
        return

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Чтобы приложение не завершалось при закрытии последнего окна

    window = MainWindow()
    tray = TrayIcon(window)

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()