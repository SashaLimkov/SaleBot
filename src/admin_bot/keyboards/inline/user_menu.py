from aiogram.types import InlineKeyboardMarkup

__all__ = [
    "get_days",

]

from admin_bot.utils.butto_worker import add_button
from admin_bot.utils.datetime_helper import get_datetime


async def get_days():
    keyboard = InlineKeyboardMarkup(row_width=1)
    yesterday = str(await get_datetime("yesterday")).split(' ')[0]
    today = str(await get_datetime("today")).split(' ')[0]
    tomorrow = str(await get_datetime("tomorrow")).split(' ')[0]
    keyboard.add(await add_button(text=yesterday, cd="yd"))
    keyboard.add(await add_button(text=today, cd="td"))
    keyboard.add(await add_button(text=tomorrow, cd="tm"))
    return keyboard
