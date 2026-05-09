from aiogram import Router, types, F
from aiogram.filters import Command
from filters.is_admin import IsAdmin
from utils.pc_api import pc_service

router = Router()
# Застосовуємо фільтр IsAdmin до всього роутера, 
# щоб тільки адмін міг керувати ПК
router.message.filter(IsAdmin())

@router.message(Command("shutdown"))
@router.message(F.text == "Вимкнути ПК")
async def cmd_shutdown(message: types.Message):
    success = await pc_service.shutdown()
    if success:
        await message.answer("Команда на вимкнення надіслана успішно! ⏻")
    else:
        await message.answer("Помилка при спробі вимкнути ПК. ❌")

@router.message(Command("reboot"))
@router.message(F.text == "Перезавантажити ПК")
async def cmd_reboot(message: types.Message):
    success = await pc_service.reboot()
    if success:
        await message.answer("Команда на перезавантаження надіслана! 🔄")
    else:
        await message.answer("Помилка при спробі перезавантажити ПК. ❌")

@router.message(Command("stats"))
@router.message(F.text == "Статистика ПК")
async def cmd_stats(message: types.Message):
    stats_data = await pc_service.get_stats()
    
    # TODO: Реалізувати генерацію картинки на основі stats_data
    # 1. Отримати дані з stats_data (json)
    # 2. Використати бібліотеку Pillow або подібну для малювання графіків/тексту
    # 3. Надіслати картинку як InputFile
    
    # Тимчасова відповідь текстом
    stats_text = (
        "📊 **Статистика ПК**\n\n"
        f"CPU: {stats_data['cpu_usage']}%\n"
        f"RAM: {stats_data['ram_usage']}%\n"
        f"Temp: {stats_data['temp']}°C\n"
        f"Uptime: {stats_data['uptime']}"
    )
    
    await message.answer(stats_text, parse_mode="Markdown")
    # Після реалізації генерації картинки:
    # await message.answer_photo(photo=generated_image, caption="Поточна статистика")
