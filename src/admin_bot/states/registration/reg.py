from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistration(StatesGroup):
    registration = State()
    name = State()
    second_name = State()
    number = State()
    email = State()
    city = State()
