from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

import config
import texts
from functions import func

main_menu_btn = [
    "Поддержка",
]

admin_menu_btn = [
    '🤖Админка',
]


def main_menu(user_id=0):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(main_menu_btn[0])
    if user_id == config.admin_id:
        markup.add(admin_menu_btn[0])
    return markup


def support_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="🆘 Support", url=f"https://t.me/{config.admin_username}")
    )
    return markup


admin_menu = InlineKeyboardMarkup(row_width=1)
admin_menu.add(
    InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
    InlineKeyboardButton(text="🗣 Рассылка", callback_data="admin_mail"),
    InlineKeyboardButton(text="🔎 Найти юзера", callback_data="admin_search"),
)


def settings_user(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="🔙 Назад", callback_data="admin_menu"),
    )
    return markup


def markup(text, call_data):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text=text, callback_data=call_data)
    )
    return markup
