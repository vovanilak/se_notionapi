import asyncio
import logging
import sys
import os
from os import getenv
from bot.handlers import start
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("MY_BOT_TOKEN")
dp = Dispatcher()

async def main():
    bt = Bot(TOKEN)
    await bt.delete_webhook(drop_pending_updates=True)
    dp.include_routers(
        start.router
    )
    
    await dp.start_polling(bt)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())