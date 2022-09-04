from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.services.db.settings_user import (
    update_currency_settings_user,
    get_currency_settings_user,
)


async def select_cur(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    cur = callback_data["cur"]
    chat_id = call.message.chat.id
    await update_currency_settings_user(user_id=chat_id, currency=cur)
    await call.answer("Валюта обновлена")
    try:
        selected = await get_currency_settings_user(chat_id)
        await bot.edit_message_text(
            chat_id=chat_id,
            text=td.MM_S_CUR.format(cur=selected),
            message_id=call.message.message_id,
            reply_markup=await ik.select_cur(callback_data),
        )
    except:
        pass
