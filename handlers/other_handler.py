from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.callback_query_handler(text=".", state='*')
async def handler_call_dot(call: types.CallbackQuery, state: FSMContext):
    pass


@dp.callback_query_handler(state='*')
async def handler_call(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
