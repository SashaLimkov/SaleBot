from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.utils.state_worker import state_update_fields, short_link_worker
from bot.data import text_data as td
from bot.keyboards import inline as ik


async def short_link(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = call.message.chat.id
    data = await short_link_worker(
        state=state, user_id=user_id, callback_data=callback_data, add_data=True
    )
    await bot.edit_message_text(
        chat_id=user_id,
        text=td.MM_SH_LINK,
        message_id=call.message.message_id,
        reply_markup=await ik.short_link(callback_data, data["Link"]),
    )


async def cancel_short_link(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    user_id = call.message.chat.id
    data = await short_link_worker(
        state=state,
        user_id=user_id,
        callback_data=callback_data,
    )
    await bot.edit_message_text(
        chat_id=user_id,
        text=td.MM_SH_LINK,
        message_id=call.message.message_id,
        reply_markup=await ik.short_link(callback_data, data["Link"]),
    )
