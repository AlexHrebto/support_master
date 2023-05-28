import asyncio
import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from keyboards import menu
from functions import func
from filters import *
from states import *


@dp.message_handler(IsAdmin(), text=menu.admin_menu_btn[0], state='*')
@dp.message_handler(IsAdmin(), commands=['admin'], state='*')
async def handler_admin_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Меню админа</b>", reply_markup=menu.admin_menu)


@dp.callback_query_handler(state='*', regexp=r"^admin_menu$")
async def handler_call_admin_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<b>Меню админа</b>", reply_markup=menu.admin_menu)


@dp.callback_query_handler(state='*', regexp=r"^admin_stats$")
async def handler_call_admin_stats(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    text = func.admin_stats()
    if call.message.html_text not in text:
        await call.message.edit_text(text, reply_markup=menu.admin_menu)


@dp.callback_query_handler(state='*', regexp=r"^view_user:\d+$")
async def handler_call_view_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.data.split(':')[1]
    user = func.User(user_id)
    text = f"""
<b>Пользователь</b>
<b>📍 ID:</b> <a href="tg://user?id={user_id}">{user_id}</a>
<b>📜 Дата регистрации:</b> <i>{str(user.date_reg)[:10]}</i>
<b>👥 Пришел от:</b> <a href="tg://user?id={user.ref_code}">{user.ref_code}</a>
"""
    await call.message.edit_text(text, reply_markup=menu.settings_user(user_id))


@dp.callback_query_handler(state='*', regexp=r"^admin_search$")
async def handler_call_admin_search(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await SearchUser.user_id.set()
    await call.message.edit_text("Введите ID пользователя", reply_markup=menu.markup("🔙 Назад", "admin_menu"))


@dp.message_handler(IsAdmin(), state=SearchUser.user_id)
async def handler_admin_search_user_id(message: types.Message, state: FSMContext):
    msg = message.text
    if msg.isdigit() and 8 <= len(msg) <= 12:
        await state.finish()
        user = func.User(msg)
        if user.id:
            text = f"""
<b>Пользователь</b>
<b>📍 ID:</b> <a href="tg://user?id={user.user_id}">{user.user_id}</a>
<b>📜 Дата регистрации:</b> <i>{str(user.date_reg)[:10]}</i>
<b>👥 Пришел от:</b> <a href="tg://user?id={user.ref_code}">{user.ref_code}</a>
"""

            await message.answer(text, reply_markup=menu.settings_user(user.user_id))
        else:
            await message.answer("Пользователь не найден", reply_markup=menu.admin_menu)
    else:
        await message.answer("Введите ID пользователя")


@dp.callback_query_handler(state='*', regexp=r"^admin_mail$")
async def handler_call_admin_mail(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await Email.message_id.set()
    await call.message.edit_text("Отправьте сообщение для рассылки (текст, фото, видео или гиф)")


@dp.message_handler(IsAdmin(), state=Email.message_id, content_types=['text', 'photo', 'video', 'gif', 'animation'])
async def handler_admin_mail_message_id(message: types.Message, state: FSMContext):
    message_id = message.message_id
    await state.update_data(message_id=message_id)
    await Email.next()
    await bot.copy_message(message.from_user.id, message.from_user.id, message_id)
    await message.answer("Отправьте + для подтверждения")


@dp.message_handler(state=Email.confirm)
async def handler_admin_mail_confirm(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            message_id = data['message_id']
        await state.finish()
        asyncio.create_task(send_email(message, message_id))
    else:
        await state.finish()
        await message.answer("Рассылка отменена")


async def send_email(message, message_id):
    users = func.get_all_users()
    await message.answer(f"Рассылка началась\nВсего пользователей: {len(users)}")
    time_start = time.time()
    true_send = 0
    for user_id, in users:
        try:
            await bot.copy_message(user_id, message.from_user.id, message_id)
            true_send += 1
            await asyncio.sleep(0.15)
        except:
            pass
    text = f"""
✅ Рассылка окончена
👍 Отправлено: {true_send}
👎 Не отправлено: {len(users) - true_send}
🕐 Время выполнения: {int(float(str(time.time() - time_start)))} секунд
"""
    await message.answer(text)
