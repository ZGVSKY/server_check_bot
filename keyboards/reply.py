from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Статистика ПК"), KeyboardButton(text="Зробити скріншот")],
            [KeyboardButton(text="Гучність -"), KeyboardButton(text="Без звуку"), KeyboardButton(text="Гучність +")],
            [KeyboardButton(text="Вимкнути ПК"), KeyboardButton(text="Перезавантажити ПК")],
            [KeyboardButton(text="Допомога")]
        ],
        resize_keyboard=True
    )
