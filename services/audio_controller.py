# Альтернативный способ
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

class AudioController:
    def __init__(self):
        sessions = AudioUtilities.GetAllSessions()
        # Находим устройство вывода
        self.volume = None
        for session in sessions:
            if session.Process and session.Process.name() == "SystemSounds":
                # Это не то
                continue
        # Проще: получить дефолтное устройство
        devices = AudioUtilities.GetSpeakers()
        self.volume = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        # Если выше падает, пробуем через IMMDevice
        if not self.volume:
            from pycaw.pycaw import IMMDeviceEnumerator
            enumerator = IMMDeviceEnumerator()
            device = enumerator.GetDefaultAudioEndpoint(0, 0)
            self.volume = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)