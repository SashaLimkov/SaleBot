from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.handlers.user import cleaner, registration, commands


def setup(dp: Dispatcher):
    dp.register_errors_handler(commands.error)
    dp.register_message_handler(commands.start_cmd, filters.CommandStart(), state="*")
    registration.setup(dp)
    dp.register_message_handler(cleaner.clean_s)
