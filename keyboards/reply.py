from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard(is_superuser: bool = False):
    buttons = [
        [KeyboardButton(text="Статистика ПК"), KeyboardButton(text="Зробити скріншот")],
        [KeyboardButton(text="Гучність -"), KeyboardButton(text="Без звуку"), KeyboardButton(text="Гучність +")],
        [KeyboardButton(text="Командний рядок")],
        [KeyboardButton(text="Вимкнути ПК"), KeyboardButton(text="Перезавантажити ПК")],
    ]
    
    if is_superuser:
        buttons.append([KeyboardButton(text="Керування користувачами")])
        
    buttons.append([KeyboardButton(text="Допомога")])
    
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
