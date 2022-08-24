from aiogram.types import InlineKeyboardMarkup

__all__ = [
    "get_days",

]

from admin_bot.utils.butto_worker import add_button
from admin_bot.utils.datetime_helper import get_datetime
from admin_bot.data import callback_data as cd


async def get_days():
    keyboard = InlineKeyboardMarkup(row_width=1)
    yesterday = str(await get_datetime("yesterday")).split(' ')[0]
    today = str(await get_datetime("today")).split(' ')[0]
    tomorrow = str(await get_datetime("tomorrow")).split(' ')[0]
    keyboard.add(await add_button(text=yesterday, cd=cd.date.new(
        day="yt"
    )))
    keyboard.add(await add_button(text=today, cd=cd.date.new(
        day="td"
    )))
    keyboard.add(await add_button(text=tomorrow,cd=cd.date.new(
        day="tm"
    )))
    return keyboard
