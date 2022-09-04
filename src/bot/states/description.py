from aiogram.dispatcher.filters.state import StatesGroup, State


class AddData(StatesGroup):
    INPUT = State()
    ADD_DOCUMENT = State()
    CHANGE_C = State()


class BaseState(StatesGroup):
    BASE = State()
