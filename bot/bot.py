import asyncio
from os import getenv
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.handlers import router

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

TOKEN = getenv("TELEGRAM_TOKEN")


dp = Dispatcher()
dp.include_router(router=router)


async def main() -> None:
    bot = Bot(token=TOKEN)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
