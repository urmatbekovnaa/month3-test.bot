import asyncio
import logging
from aiogram import Bot


from bot_config import dp, bot, database
from handlers.start import start_router
from handlers.send_dialog import send_dialog_router

async def on_startup(bot: Bot):
    print("Бот запустился")
    database.create_table()

async def main():
    dp.include_router(start_router)
    dp.include_router(send_dialog_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
