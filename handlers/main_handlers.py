from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from loader import dp, bot
from keyboards import menu
from functions import func
import texts


@dp.message_handler(chat_type="private", commands=['start'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await func.first_join(message.from_user.id, message.from_user.username, message.text)
    await message.answer(texts.start.format(config.admin_username), reply_markup=menu.main_menu(message.from_user.id))


@dp.message_handler(chat_type="private", text=menu.main_menu_btn[0], state='*')
async def handler_support(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.support, reply_markup=menu.support_menu())
    func.update_username(message.from_user.id, message.from_user.username)


@dp.message_handler(chat_type="private", content_types=types.ContentType.ANY)
async def handler_support(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    await bot.send_message(config.admin_id, f"Сообщение от @{username} (<a href='tg://user?id={user_id}'>{user_id}</a>)")
    await bot.forward_message(config.admin_id, user_id, message.message_id)

