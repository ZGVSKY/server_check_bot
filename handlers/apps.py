from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from filters.permissions import HasPermission
from database.apps_db import apps_db
from keyboards.inline import get_apps_kb, get_apps_manage_kb
from utils.pc_api import pc_service
import os

router = Router()

class AppStates(StatesGroup):
    waiting_for_path = State()
    waiting_for_name = State()

@router.message(F.text == "Додати в швидкий запуск", HasPermission("full"))
async def add_app_start(message: types.Message, state: FSMContext):
    await message.answer("📂 Введіть повний шлях до файлу .exe або посилання (напр. `C:\\Games\\wow.exe`):")
    await state.set_state(AppStates.waiting_for_path)

@router.message(AppStates.waiting_for_path, HasPermission("full"))
async def add_app_path(message: types.Message, state: FSMContext):
    path = message.text.strip()
    await state.update_data(path=path)
    
    # Спробуємо витягнути назву з шляху автоматично
    auto_name = os.path.basename(path).replace(".exe", "").capitalize()
    
    await message.answer(
        f"✅ Шлях отримано.\nТепер введіть назву для цієї програми (або надішліть `+`, щоб використати назву `{auto_name}`):"
    )
    await state.set_state(AppStates.waiting_for_name)

@router.message(AppStates.waiting_for_name, HasPermission("full"))
async def add_app_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    path = data['path']
    name = message.text.strip()
    
    if name == "+":
        name = os.path.basename(path).replace(".exe", "").capitalize()
        
    apps_db.add_app(name, path)
    await state.clear()
    await message.answer(f"🌟 Програму `{name}` успішно додано до списку!")

@router.message(F.text == "Запуск програм", HasPermission("stats_only"))
async def list_apps(message: types.Message):
    apps = apps_db.get_apps()
    if not apps:
        await message.answer("Списку програм поки немає. Додайте щось через кнопку 'Додати в швидкий запуск'.")
        return
        
    await message.answer("🚀 Оберіть програму для запуску:", reply_markup=get_apps_kb(apps))

@router.callback_query(F.data.startswith("launch:"))
async def launch_app_handler(callback: types.CallbackQuery):
    idx = int(callback.data.split(":")[1])
    apps = apps_db.get_apps()
    
    if idx >= len(apps):
        await callback.answer("Помилка: програму не знайдено.")
        return
        
    app = apps[idx]
    await callback.message.edit_text(f"⏳ Запускаю `{app['name']}`...")
    
    success = await pc_service.launch_app(app['path'])
    if success:
        await callback.message.edit_text(f"✅ Програму `{app['name']}` успішно запущено!")
    else:
        await callback.message.edit_text(f"❌ Не вдалося запустити `{app['name']}`. Перевірте шлях або статус API.")
