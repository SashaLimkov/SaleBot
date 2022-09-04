from aiogram.dispatcher.filters.state import StatesGroup, State


class PostAdding(StatesGroup):
    adding = State()
    album = State()
