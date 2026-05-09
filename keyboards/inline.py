from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_request_kb(user_id: int, username: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Заборонити", callback_data=f"perm:unauthorized:{user_id}"),
        ],
        [
            InlineKeyboardButton(text="Тільки Статистика", callback_data=f"perm:stats_only:{user_id}"),
        ],
        [
            InlineKeyboardButton(text="Повний Доступ", callback_data=f"perm:full:{user_id}"),
        ]
    ])

def get_user_manage_kb(users: dict):
    buttons = []
    for uid, data in users.items():
        buttons.append([InlineKeyboardButton(
            text=f"{data['username']} ({data['permission']})", 
            callback_data=f"manage:{uid}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_user_edit_kb(user_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Встановити: Тільки Статистика", callback_data=f"perm:stats_only:{user_id}")],
        [InlineKeyboardButton(text="Встановити: Повний Доступ", callback_data=f"perm:full:{user_id}")],
        [InlineKeyboardButton(text="Видалити доступ", callback_data=f"perm:unauthorized:{user_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="manage_users")]
    ])

def get_apps_kb(apps: list):
    buttons = []
    for idx, app in enumerate(apps):
        buttons.append([InlineKeyboardButton(text=f"🚀 {app['name']}", callback_data=f"launch:{idx}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_apps_manage_kb(apps: list):
    buttons = []
    for idx, app in enumerate(apps):
        buttons.append([
            InlineKeyboardButton(text=f"❌ {app['name']}", callback_data=f"del_app:{idx}")
        ])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
