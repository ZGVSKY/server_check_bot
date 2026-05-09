from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я твій бот для керування ПК. Використовуй меню нижче:",
        reply_markup=main_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "📖 **Посібник користувача PC Control Bot**\n\n"
        "Цей бот дозволяє дистанційно керувати вашим ПК. "
        "Доступ до функцій залежить від вашого рівня прав.\n\n"
        "⚡️ **Основні команди:**\n"
        "📊 *Статистика ПК* — Отримати візуальний дашборд (CPU, RAM, Температура).\n"
        "📸 *Зробити скріншот* — Отримати поточне зображення екрана.\n"
        "🚀 *Запуск програм* — Меню швидкого запуску доданих програм.\n"
        "📂 *Додати в швидкий запуск* — Додати шлях до .exe для швидкого запуску.\n"
        "🔊 *Гучність* (+, -, Без звуку) — Керування звуком ПК.\n"
        "🖥 *Командний рядок* — Виконання команд у терміналі (cmd/powershell).\n"
        "⏻ *Вимкнути/Перезавантажити* — Керування живленням ПК.\n\n"
        "👥 **Для адміністратора:**\n"
        "⚙️ *Керування користувачами* — Надання доступу іншим та зміна їх прав.\n\n"
        "⚠️ **Автоматика:**\n"
        "Бот автоматично попередить вас, якщо температура ПК перевищить поріг."
    )
    await message.answer(help_text, parse_mode="Markdown")
