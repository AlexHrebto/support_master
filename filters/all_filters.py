from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher import filters

import config
from functions import func


# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id == config.admin_id

