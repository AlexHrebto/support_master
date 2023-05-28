from aiogram.dispatcher.filters.state import State, StatesGroup


class SendMessage(StatesGroup):
    order_id = State()
    message_id = State()


class SearchUser(StatesGroup):
    user_id = State()


class Email(StatesGroup):
    message_id = State()
    confirm = State()
