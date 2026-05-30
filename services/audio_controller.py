# services/audio_controller.py
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class AudioController:
    def __init__(self):
        # Безопасный способ получения интерфейса громкости
        try:
            # Способ 1: через GetSpeakers
            devices = AudioUtilities.GetSpeakers()
            self.volume = devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
            self.volume = self.volume.QueryInterface(IAudioEndpointVolume)
        except Exception as e1:
            app_logger.error(f"Не удалось инициализировать аудио (GetSpeakers): {e1}")
            # Способ 2: через enumerator
            try:
                from pycaw.pycaw import IMMDeviceEnumerator, EDataFlow, ERole
                enumerator = AudioUtilities.GetDeviceEnumerator()
                device = enumerator.GetDefaultAudioEndpoint(EDataFlow.eRender, ERole.eMultimedia)
                self.volume = device.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
                self.volume = self.volume.QueryInterface(IAudioEndpointVolume)
            except Exception as e2:
                app_logger.error(f"Не удалось инициализировать аудио (enumerator): {e2}")
                raise

    def get_system_volume(self):
        return int(self.volume.GetMasterVolumeLevelScalar() * 100)

    def set_system_volume(self, value: int):
        self.volume.SetMasterVolumeLevelScalar(value / 100.0, None)