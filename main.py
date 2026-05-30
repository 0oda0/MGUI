# main.py
import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from tray_icon import TrayIcon
from config_manager import ConfigManager

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

def main():
    if not is_admin():
        run_as_admin()
        return

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    config = ConfigManager()
    window = MainWindow()

    # Восстанавливаем геометрию окна, если есть
    geom = config.get("window_geometry")
    if geom:
        window.setGeometry(geom["x"], geom["y"], geom["width"], geom["height"])
    else:
        window.setGeometry(100, 100, 900, 600)

    tray = TrayIcon(window)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()