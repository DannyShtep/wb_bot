from aiogram import types

def get_main_menu_keyboard():
    """Возвращает клавиатуру главного меню."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add("Начать бронирование")
    keyboard.add("Отменить")
    return keyboard

def get_cancel_monitoring_keyboard():
    """Возвращает клавиатуру для отмены мониторинга."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add("🚫 Отменить планирование")
    return keyboard
