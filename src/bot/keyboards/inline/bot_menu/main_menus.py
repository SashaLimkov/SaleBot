from aiogram.types import InlineKeyboardMarkup

from bot.data import callback_data as cd
from bot.data import list_data as ld
from bot.utils.butto_worker import add_button
from bot.utils.datetime_helper import get_datetime


async def get_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for index, text in enumerate(ld.MAIN_MENU):
        keyboard.insert(await add_button(text=text, cd=cd.mm.new(action=index + 1)))
    return keyboard


async def back_to_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(await add_button(text="Назад", cd="back"))
    return keyboard


async def back_to_s_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        await add_button(
            text="Назад",
            cd="back_to_s_m",
        )
    )
    return keyboard


async def back_to():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=1,
            ),
        )
    )
    return keyboard


async def get_anons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    yesterday = str(await get_datetime("yt")).split(" ")[0]
    today = str(await get_datetime("td")).split(" ")[0]
    tomorrow = str(await get_datetime("tm")).split(" ")[0]
    keyboard.add(await add_button(text=yesterday, cd=f"day_{yesterday}"))
    keyboard.add(await add_button(text=today, cd=f"day_{today}"))
    keyboard.add(await add_button(text=tomorrow, cd=f"day_{tomorrow}"))
    keyboard.add(await add_button(text="Назад", cd="back"))
    return keyboard
