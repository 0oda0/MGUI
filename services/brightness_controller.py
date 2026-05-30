# services/brightness_controller.py
import screen_brightness_control as sbc
import logging

class BrightnessController:
    @staticmethod
    def get_brightness():
        try:
            values = sbc.get_brightness()
            if values and len(values) > 0:
                return values[0]
            else:
                # Если список пуст, пробуем получить для основного дисплея по-другому
                return sbc.get_brightness(display=0) if sbc.list_monitors() else 50
        except Exception as e:
            logging.error(f"Ошибка получения яркости: {e}")
            return 50  # значение по умолчанию

    @staticmethod
    def set_brightness(value: int):
        try:
            sbc.set_brightness(value)
        except Exception as e:
            logging.error(f"Ошибка установки яркости: {e}")