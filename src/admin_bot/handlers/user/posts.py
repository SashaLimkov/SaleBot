from aiogram import types
from aiogram.dispatcher import FSMContext

import admin_bot.handlers.user
from admin_bot.config.loader import bot
from admin_bot.services.db import posts as posts_db
from admin_bot.keyboards import inline as ik
from admin_bot.utils.datetime_helper import get_datetime


async def some_day_posts(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await show_post(call, callback_data["day"])


async def show_post(call: types.CallbackQuery, key):
    day = await get_datetime(key)
    posts = [post for post in await posts_db.get_post(day)]
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text="Спиосок доступных постов",
    )
    if posts:
        for post in posts:
            await bot.send_message(
                chat_id=call.message.chat.id,
                text=f"{post.description}, {post.date}"
            )
    else:
        await call.answer(text="Нет постов за этот день")
