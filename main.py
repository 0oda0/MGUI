# main.py
import sys
import ctypes
import traceback
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from tray_icon import TrayIcon
from config_manager import ConfigManager
from logger import app_logger

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    app_logger.info("Запрос прав администратора...")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

def main():
    if not is_admin():
        run_as_admin()
        return

    app_logger.info("=== MGUI запущено ===")
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    try:
        config = ConfigManager()
        window = MainWindow()

        geom = config.get("window_geometry")
        if geom:
            window.setGeometry(geom["x"], geom["y"], geom["width"], geom["height"])
        else:
            window.setGeometry(100, 100, 1200, 700)

        tray = TrayIcon(window)
        window.show()
        app_logger.info("Главное окно показано, иконка в трее создана")

        def cleanup():
            app_logger.info("Завершение приложения")
            if hasattr(window, 'game_mode_widget') and hasattr(window.game_mode_widget, 'tracker'):
                window.game_mode_widget.tracker.stop()
                app_logger.info("Трекер игр остановлен")

        app.aboutToQuit.connect(cleanup)
        sys.exit(app.exec())
    except Exception as e:
        app_logger.error(f"Критическая ошибка: {e}")
        app_logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()