# services/audio_controller.py
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

class AudioController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)

    def get_system_volume(self):
        return int(self.volume.GetMasterVolumeLevelScalar() * 100)

    def set_system_volume(self, value: int):
        self.volume.SetMasterVolumeLevelScalar(value / 100.0, None)

    def get_mic_volume(self):
        # Упрощённо — можно реализовать позже через MicrophoneEnumerator
        return 50

    def set_mic_volume(self, value: int):
        pass