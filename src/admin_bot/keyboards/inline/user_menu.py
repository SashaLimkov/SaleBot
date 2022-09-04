from aiogram.types import InlineKeyboardMarkup
from admin_bot.services.db import posts as posts_db

__all__ = ["get_days", "get_posts_by_date"]

from admin_bot.utils.butto_worker import add_button
from admin_bot.utils.datetime_helper import get_datetime
from admin_bot.data import callback_data as cd


async def get_days():
    keyboard = InlineKeyboardMarkup(row_width=1)
    yesterday = str(await get_datetime("yt")).split(" ")[0]
    today = str(await get_datetime("td")).split(" ")[0]
    tomorrow = str(await get_datetime("tm")).split(" ")[0]
    keyboard.add(await add_button(text=yesterday, cd=cd.date.new(day="yt")))
    keyboard.add(await add_button(text=today, cd=cd.date.new(day="td")))
    keyboard.add(await add_button(text=tomorrow, cd=cd.date.new(day="tm")))
    return keyboard


async def get_posts_by_date(callback_data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    day = await get_datetime(callback_data["day"])
    posts = [post for post in await posts_db.get_post(day)]
    for post in posts:
        keyboard.add(
            await add_button(
                text=post.name,
                cd=cd.posts_by_date.new(day=callback_data["day"], post=post.name),
            )
        )
    keyboard.add(
        await add_button(
            text="Добавить пост",
            cd=cd.add_post.new(
                day=callback_data["day"],
                add=1,
            ),
        )
    )
    keyboard.add(await add_button(text="Назад", cd="mm"))
    return keyboard


# async def add_post_keyboard():
