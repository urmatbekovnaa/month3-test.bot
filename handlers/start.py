from aiogram import Router, F, types, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardMarkup

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: Message):
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(text="Отправить домашнее задание", callback_data="send_homework")
            ]],
        resize_keyboard=True
        )
    await message.answer(f"Добро пожаловать {name}. \nB бот 'Bot for Homework'"
                         "для отправки домашнего задания", reply_markup=kb)

