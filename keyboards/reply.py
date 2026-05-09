from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Статистика ПК")],
            [KeyboardButton(text="Вимкнути ПК"), KeyboardButton(text="Перезавантажити ПК")],
            [KeyboardButton(text="Допомога")]
        ],
        resize_keyboard=True
    )
