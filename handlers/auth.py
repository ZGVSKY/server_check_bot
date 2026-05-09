from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from config import config
from database.user_db import user_db
from keyboards.reply import main_keyboard
from keyboards.inline import get_admin_request_kb, get_user_manage_kb, get_user_edit_kb
from filters.permissions import IsSuperuser

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.full_name
    
    # 1. Якщо це Суперкористувач
    if user_id == config.admin_id:
        await message.answer(
            f"Привіт, Суперкористувач {username}! Панель керування активована.",
            reply_markup=main_keyboard(is_superuser=True)
        )
        return

    # 2. Перевірка існуючих прав
    user_data = user_db.get_user(str(user_id))
    if user_data:
        perm = user_data.get("permission", "unauthorized")
        if perm != "unauthorized":
            await message.answer(
                f"Вітаємо знову! Ваш рівень доступу: {perm}",
                reply_markup=main_keyboard(is_superuser=False)
            )
            return

    # 3. Якщо новий користувач - запит до адміна
    await message.answer("Ваш запит на доступ надіслано адміністратору. Очікуйте підтвердження.")
    
    await bot.send_message(
        config.admin_id,
        f"🔔 **Новий запит на доступ!**\nКористувач: {username} (ID: {user_id})",
        reply_markup=get_admin_request_kb(user_id, username)
    )

# --- Керування користувачами (Тільки для Суперкористувача) ---

@router.message(F.text == "Керування користувачами", IsSuperuser())
@router.callback_query(F.data == "manage_users", IsSuperuser())
async def cmd_manage_users(event: types.Message | types.CallbackQuery):
    users = user_db.get_all_users()
    kb = get_user_manage_kb(users)
    text = "👥 Список користувачів та їх права:"
    
    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=kb)
    else:
        await event.message.edit_text(text, reply_markup=kb)

@router.callback_query(F.data.startswith("manage:"), IsSuperuser())
async def process_manage_user(callback: types.CallbackQuery):
    user_id = callback.data.split(":")[1]
    user_data = user_db.get_user(user_id)
    
    if not user_data:
        await callback.answer("Користувача не знайдено.")
        return
        
    await callback.message.edit_text(
        f"Редагування прав для: {user_data['username']}\nПоточні права: {user_data['permission']}",
        reply_markup=get_user_edit_kb(user_id)
    )

# --- Обробка зміни прав ---

@router.callback_query(F.data.startswith("perm:"), IsSuperuser())
async def process_permission_change(callback: types.CallbackQuery, bot: Bot):
    _, permission, user_id = callback.data.split(":")
    
    # Отримуємо ім'я користувача (можна спробувати з бази)
    old_data = user_db.get_user(user_id)
    username = old_data['username'] if old_data else "Unknown"
    
    user_db.set_permission(user_id, permission, username)
    
    await callback.answer(f"Права змінено на: {permission}")
    await callback.message.edit_text(f"✅ Користувачу {username} встановлено права: {permission}")
    
    # Сповіщаємо користувача
    try:
        if permission == "unauthorized":
            await bot.send_message(user_id, "❌ Ваш доступ до бота було скасовано або відхилено.")
        else:
            await bot.send_message(
                user_id, 
                f"✅ Адміністратор надав вам доступ! Рівень: {permission}",
                reply_markup=main_keyboard(is_superuser=False)
            )
    except Exception:
        pass
