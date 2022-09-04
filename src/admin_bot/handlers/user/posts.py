from aiogram import types
from aiogram.dispatcher import FSMContext

import admin_bot.handlers.user
from admin_bot.config.loader import bot
from admin_bot.services.db import posts as posts_db
from admin_bot.keyboards import inline as ik
from admin_bot.utils.datetime_helper import get_datetime


async def show_post(call: types.CallbackQuery, callback_data):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text="Список доступных постов",
        message_id=call.message.message_id,
        reply_markup=await ik.get_posts_by_date(callback_data),
    )


async def add_post_menu(call: types.CallbackQuery, callback_data, state):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text="Список доступных постов",
        message_id=call.message.message_id,
        reply_markup=await ik.get_posts_by_date(callback_data),
    )
