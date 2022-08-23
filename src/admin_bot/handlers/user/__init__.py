from aiogram import Dispatcher, types
from aiogram.dispatcher import filters

from admin_bot.handlers.user import cleaner, commands
from admin_bot.middleware import AlbumMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(AlbumMiddleware())
    dp.register_errors_handler(commands.error)
    dp.register_message_handler(commands.start_cmd, filters.CommandStart(), state="*")
    dp.register_message_handler(cleaner.clean_s, is_media_group=True,
                                content_types=types.ContentType.ANY)
