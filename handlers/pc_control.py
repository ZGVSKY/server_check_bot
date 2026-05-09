from aiogram import Router, types, F
from aiogram.filters import Command
from filters.permissions import HasPermission
from utils.pc_api import pc_service

router = Router()

@router.message(Command("shutdown"), HasPermission("full"))
@router.message(F.text == "Вимкнути ПК", HasPermission("full"))
async def cmd_shutdown(message: types.Message):
    success = await pc_service.shutdown()
    if success:
        await message.answer("Команда на вимкнення надіслана успішно! ⏻")
    else:
        await message.answer("Помилка при спробі вимкнути ПК. ❌")

@router.message(Command("reboot"), HasPermission("full"))
@router.message(F.text == "Перезавантажити ПК", HasPermission("full"))
async def cmd_reboot(message: types.Message):
    success = await pc_service.reboot()
    if success:
        await message.answer("Команда на перезавантаження надіслана! 🔄")
    else:
        await message.answer("Помилка при спробі перезавантажити ПК. ❌")

@router.message(Command("screenshot"), HasPermission("full"))
@router.message(F.text == "Зробити скріншот", HasPermission("full"))
async def cmd_screenshot(message: types.Message):
    await message.answer("📸 Роблю скріншот...")
    path = await pc_service.take_screenshot()
    if path:
        photo = types.FSInputFile(path)
        await message.answer_photo(photo=photo, caption="🖥 Скріншот робочого столу")
    else:
        await message.answer("❌ Не вдалося отримати скріншот. Перевірте, чи працює API.")

@router.message(F.text.in_(["Гучність +", "Гучність -", "Без звуку"]), HasPermission("full"))
async def cmd_volume(message: types.Message):
    actions = {
        "Гучність +": "up",
        "Гучність -": "down",
        "Без звуку": "mute"
    }
    action = actions[message.text]
    success = await pc_service.set_volume(action)
    if success:
        await message.answer(f"Дія '{message.text}' виконана успішно! 🔊")
    else:
        await message.answer("Помилка при зміні гучності. ❌")

from utils.image_gen import create_stats_image

@router.message(Command("stats"), HasPermission("stats_only"))
@router.message(F.text == "Статистика ПК", HasPermission("stats_only"))
async def cmd_stats(message: types.Message):
    await message.answer("🔄 Отримую дані...")
    stats_data = await pc_service.get_stats()
    
    # Генеруємо картинку
    image_path = create_stats_image(stats_data)
    
    photo = types.FSInputFile(image_path)
    await message.answer_photo(
        photo=photo, 
        caption=f"📊 **Статистика ПК**\nПоточний стан на {stats_data.get('uptime')}",
        parse_mode="Markdown"
    )
