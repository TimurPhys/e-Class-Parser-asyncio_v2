import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.auth import router
from middlewares.db import DataBaseSession
from database.engine import create_db, session_maker

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    await create_db()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")