from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_config import database

send_dialog_router = Router()

class Form(StatesGroup):
    name = State()
    ggroup = State()
    homework = State()
    link = State()

@send_dialog_router.message(F.data == "send_homework")
async def start_send_homework_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    await callback.message.answer("Доброго времени суток.\n"
                                  "Введите ваше имя:")
    await callback.answer()


@send_dialog_router.message(Command("stop"))
async def stop_handler(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили отправку домашнего задания.")
    await state.clear()


@send_dialog_router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.ggroup)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Python 46-1"),
                types.KeyboardButton(text="Python 46-2"),
            ],
            [
                types.KeyboardButton(text="Python 47-1"),
                types.KeyboardButton(text="Python 47-2"),
            ],
            [
                types.KeyboardButton(text="Python 48-1"),
                types.KeyboardButton(text="Python 48-2"),
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите свою группу", reply_markup=kb)

@send_dialog_router.message(Form.ggroup)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(Form.homework)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4"),
            ],
            [
                types.KeyboardButton(text="5"),
                types.KeyboardButton(text="6"),
                types.KeyboardButton(text="7"),
                types.KeyboardButton(text="8"),
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите ваше домашнее задание", reply_markup=kb)


@send_dialog_router.message(Form.homework)
async def process_homework(message: types.Message, state: FSMContext):
    homework = message.text
    if homework not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        await message.answer("Введите корректное число")
        return
    await state.update_data(homework=message.text)
    await state.set_state(Form.link)
    await message.answer("Введите ссылку на github репозитория")


@send_dialog_router.message(Form.link)
async def process_link(message: types.Message, state: FSMContext):
    if not message.text.startswith("https://github.com/"):
        await message.answer("Ссылка должна начинаться с https://github.com/")
        return

    await state.update_data(link=message.text)
    data = await state.get_data()


    query= "INTO homework (name, ggroup, homework, link)"
    "VALUES (?, ?, ?, ?)",
    params=(
        data['name'],
        data['ggroup'],
        data['homework'],
        data['link'])

    database.execute(query, params)

    await state.clear()
    await message.answer("Спасибо! Ваше домашнее задание отправлено.")
