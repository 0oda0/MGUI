# services/game_tracker.py
import threading
import time
import win32gui
import win32process
import psutil
from PyQt6.QtCore import QObject, pyqtSignal

class GameTracker(QObject):
    game_changed = pyqtSignal(str)  # испускается, когда текущая игра изменилась

    def __init__(self):
        super().__init__()
        self.current_game = None
        self.running = False
        self.thread = None

        # Список известных игр (по имени процесса). Можно расширять.
        self.game_processes = {
            "Cyberpunk2077.exe": "Cyberpunk 2077",
            "EldenRing.exe": "Elden Ring",
            "csgo.exe": "Counter-Strike: GO",
            "cs2.exe": "Counter-Strike 2",
            "VALORANT-Win64-Shipping.exe": "Valorant",
            "GTA5.exe": "GTA V",
            "Minecraft.Windows.exe": "Minecraft",
            "java.exe": "Minecraft (Java)",
            "RustClient.exe": "Rust",
            "FortniteClient-Win64-Shipping.exe": "Fortnite",
            "ApexLegends.exe": "Apex Legends",
            "Hearthstone.exe": "Hearthstone",
            "Diablo IV.exe": "Diablo IV",
            "League of Legends.exe": "League of Legends",
            "RocketLeague.exe": "Rocket League",
            "Warframe.x64.exe": "Warframe",
            "TheSims4.exe": "The Sims 4",
        }

    def start(self):
        """Запуск трекера в отдельном потоке."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._track_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Остановка трекера."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def _track_loop(self):
        while self.running:
            try:
                # Получаем активное окно
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid:
                    process = psutil.Process(pid)
                    process_name = process.name()
                    game_name = self._identify_game(process_name)
                    if game_name != self.current_game:
                        self.current_game = game_name
                        self.game_changed.emit(game_name)
            except Exception:
                # Если не удалось определить, сбрасываем текущую игру
                if self.current_game is not None:
                    self.current_game = None
                    self.game_changed.emit("")
            time.sleep(1)  # проверяем каждую секунду

    def _identify_game(self, process_name):
        """По имени процесса возвращает человеческое название игры или None."""
        return self.game_processes.get(process_name)