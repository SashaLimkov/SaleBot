from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.keyboards import inline as ik
from bot.data import text_data as td
from bot.services.db.settings_user import (
    update_signature_settings_user,
    get_signature_settings_user,
)
from bot.states.description import AddData
from bot.utils import deleter


async def description_settings(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    act = callback_data["act"]
    chat_id = call.message.chat.id
    data = await state.get_data()
    await state.update_data(cd=callback_data)
    if act == "1":
        await AddData.INPUT.set()
        await bot.edit_message_text(
            chat_id=chat_id,
            text="Введите свою подпись",
            message_id=call.message.message_id,
        )
    elif act == "2":
        await update_signature_settings_user(call.message.chat.id, "")
        await call.answer(text="Подпись удалена")
        sign = await get_signature_settings_user(chat_id)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=td.MM_SIGN.format(sign=sign if sign else "отсутствует"),
            reply_markup=await ik.signature(
                callback_data=data.get("cd"), user_id=chat_id
            ),
        )


async def set_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    m_mes = data.get("main_menu")
    chat_id = message.chat.id
    await deleter.delete_user_message(message)
    await deleter.delete_mes(chat_id, m_mes)
    await update_signature_settings_user(chat_id, message.text)
    sign = await get_signature_settings_user(chat_id)
    mes = await bot.send_message(
        chat_id=chat_id,
        text=td.MM_SIGN.format(sign=sign if sign else "отсутствует"),
        reply_markup=await ik.signature(callback_data=data.get("cd"), user_id=chat_id),
    )
    await state.update_data(main_menu=mes.message_id)
