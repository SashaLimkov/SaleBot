from aiogram import types
from aiogram.dispatcher import FSMContext

import admin_bot.handlers.user
from admin_bot.config.loader import bot
from admin_bot.services.db import posts as posts_db

from admin_bot.utils.datetime_helper import get_datetime


async def yesterday_posts(call: types.CallbackQuery, state: FSMContext):
    await show_post(call, "yesterday")


async def today_posts(call: types.CallbackQuery, state: FSMContext):
    await show_post(call, "today")


async def tommorow_posts(call: types.CallbackQuery, state: FSMContext):
    await show_post(call, "tomorrow")


async def show_post(call: types.CallbackQuery, key):
    day = await get_datetime(key)
    posts = [post for post in await posts_db.get_post(day)]
    if posts:
        for post in posts:
            await bot.send_message(
                chat_id=call.message.chat.id,
                text=f"{post.description}, {post.date}"
            )
    else:
        await call.answer(text="Нет постов за этот день")
