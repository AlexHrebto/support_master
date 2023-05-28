from datetime import datetime, timedelta
import sqlite3

import pytz
import asyncio

from aiogram.types import InlineKeyboardMarkup

import config
from loader import bot


def connect():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    return conn, cursor


def get_date():
    date = datetime.now(pytz.timezone("Europe/Moscow"))
    date = date.replace(tzinfo=None)
    return date


async def first_join(user_id: int, username, code: str):
    conn, cursor = connect()
    cursor.execute(f"SELECT username FROM users WHERE user_id = {user_id}")
    row = cursor.fetchone()
    if not row:
        who_invite = code[7:]

        if not who_invite.isdigit():
            who_invite = 0
        cursor.execute(f"INSERT INTO users (user_id, username, date_reg, ref_code) VALUES (?, ?, ?, ?)",
                       [user_id, username, get_date(), who_invite])
    else:
        if username and row[0] != username:
            cursor.execute(f"UPDATE users SET username = ? WHERE user_id = ?", [username, user_id])
            cursor.execute(f"UPDATE users SET username = '' WHERE username = ? AND user_id != ?", [username, user_id])
    conn.commit()
    conn.close()
    if not row:
        return True
    return False


class User:
    def __init__(self, user_id, username=''):
        conn, cursor = connect()
        cursor.execute("SELECT id, user_id, username, date_reg, ref_code FROM users WHERE user_id = ?",
                       [user_id])
        row = cursor.fetchone()
        conn.close()
        self.id = 0
        if row:
            self.id = row[0]
            self.user_id = row[1]
            self.username = row[2]
            self.date_reg = row[3]
            self.ref_code = row[4]
            if username and self.username != username:
                if username:
                    conn, cursor = connect()
                    cursor.execute(f"UPDATE users SET username = ? WHERE user_id = ?", [username, user_id])
                    cursor.execute(f"UPDATE users SET username = '' WHERE username = ? AND user_id != ?",
                                   [username, user_id])
                    conn.commit()
                    conn.close()


def get_all_users():
    conn, cursor = connect()
    cursor.execute(f"SELECT user_id FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows



async def send_all_admins(text, markup=InlineKeyboardMarkup()):
    await bot.send_message(config.admin_id, text, reply_markup=markup)
    # for chat_id in config.admin_id:
    #     try:
    #         await bot.send_message(chat_id, text, reply_markup=markup)
    #         await asyncio.sleep(0.3)
    #     except:
    #         pass


def update_username(user_id, username):
    if username:
        conn, cursor = connect()
        cursor.execute(f"UPDATE users SET username = ? WHERE user_id = ?", [username, user_id])
        cursor.execute(f"UPDATE users SET username = '' WHERE username = ? AND user_id != ?", [username, user_id])
        conn.commit()
        conn.close()


def admin_stats():
    conn, cursor = connect()
    cursor.execute("SELECT COUNT(id) FROM users")
    count_users, = cursor.fetchone()
    conn.close()
    text = f"""
<b>Статистика</b>

<b>Всего пользователей:</b> <i>{count_users}</i>
"""
    return text
