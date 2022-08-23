from aiogram import Dispatcher
from admin_bot.handlers import user, admin


def setup(dp: Dispatcher):
    user.setup(dp)
