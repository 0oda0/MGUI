# services/brightness_controller.py
import screen_brightness_control as sbc
import logging

logger = logging.getLogger(__name__)

class BrightnessController:
    @staticmethod
    def get_brightness():
        try:
            brightness = sbc.get_brightness()
            if brightness and len(brightness) > 0:
                return brightness[0]
            else:
                return 50  # значение по умолчанию
        except Exception as e:
            logger.error(f"Ошибка получения яркости: {e}")
            return 50

    @staticmethod
    def set_brightness(value: int):
        try:
            sbc.set_brightness(value)
        except Exception as e:
            logger.error(f"Ошибка установки яркости: {e}")