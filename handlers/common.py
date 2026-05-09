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
    await message.answer("Це меню допомоги.")
