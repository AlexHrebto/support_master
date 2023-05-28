# - *- coding: utf- 8 - *-
import asyncio

from aiogram import executor

import middlewares
from handlers import dp
from loader import bot


async def on_startup(dp):
    middlewares.setup(dp)
    info = await bot.get_me()
    print(f"~~~~~ Bot @{info.username} was started ~~~~~")


if __name__ == "__main__":

    executor.start_polling(dp, on_startup=on_startup)
