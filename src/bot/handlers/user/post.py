import glob
import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.services.db.settings_user import (
    update_logo_settings_user,
    delete_logo_settings_user,
)
from bot.states.description import AddData
from bot.utils import deleter
from bot.utils.state_worker import state_update_watermark
from bot.data import text_data as td
from bot.keyboards import inline as ik


async def photo_menu(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    data = await state.get_data()
    is_photo = data.get("photo", False)
    m_mes = data.get("main_menu", call.message.message_id)
    await deleter.delete_mes(chat_id, m_mes)
    mes = await bot.send_message(
        chat_id=chat_id,
        text=td.MM_POST if is_photo else td.MM_ADD_PHOTO,
        reply_markup=await ik.add_photo(
            {"action": 1, "settings": 3},
            data["Watermark"] if "Watermark" in data else [],
            is_photo,
        ),
    )
    await state.update_data(main_menu=mes.message_id)


async def add_photo(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    m_mes = data.get("main_menu", call.message.message_id)
    chat_id = call.message.chat.id
    try:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            text="Загрузите фото",
            message_id=call.message.message_id,
            reply_markup=await ik.back_to_s_menu(),
        )
    except:
        await deleter.delete_mes(chat_id, m_mes)
        mes = await bot.send_message(
            chat_id=call.message.chat.id,
            text="Загрузите фото",
            reply_markup=await ik.back_to_s_menu(),
        )
        await state.update_data(main_menu=mes.message_id)

    await AddData.ADD_DOCUMENT.set()


async def photo_keeper(message: types.Message, state: FSMContext):
    data = await state.get_data()
    m_mes = data.get("main_menu", message.message_id)
    if "document" not in message:
        await deleter.delete_user_message(message)
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                text="Необходимо загрузить несжатое фото",
                message_id=m_mes,
                reply_markup=await ik.back_to_s_menu(),
            )
        except:
            pass
    else:
        chat_id = message.chat.id
        document = message.document
        await deleter.delete_user_message(message)
        await deleter.delete_mes(chat_id, m_mes)
        mes = await bot.send_document(
            chat_id=chat_id,
            caption="Загрузите новое фото, если хотите его изменить",
            document=document.file_id,
            reply_markup=await ik.save_photo(),
        )
        file_type = document.file_name.split(".")[-1]
        await message.document.download(
            destination_file=f"photos/{chat_id}.{file_type}"
        )
        await state.update_data(main_menu=mes.message_id)
        await AddData.ADD_DOCUMENT.set()


async def save_photo(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    file = glob.glob(f"photos/{chat_id}.*")[0]
    await state.update_data(photo=file)
    print(1111)
    print(file)
    await update_logo_settings_user(chat_id, file)
    print(3333)
    data = await state.get_data()
    is_photo = data.get("photo", False)
    await deleter.delete_mes(chat_id, call.message.message_id)
    mes = await bot.send_photo(
        photo=types.InputFile(is_photo),
        chat_id=chat_id,
        caption=td.MM_POST if is_photo else td.MM_ADD_PHOTO,
        reply_markup=await ik.add_photo(
            {"action": 1, "settings": 3},
            data["Watermark"] if "Watermark" in data else [],
            is_photo,
        ),
    )
    await state.update_data(main_menu=mes.message_id)


async def select_watermark(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state_update_watermark(
        state=state,
        user_id=call.from_user.id,
        callback_data=callback_data,
        add_data=True,
    )
    await bot.edit_message_caption(
        chat_id=call.message.chat.id,
        caption=td.MM_POST,
        message_id=call.message.message_id,
        reply_markup=await ik.add_watermark(callback_data, data["Watermark"]),
    )


async def cancel_selection_watermark(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state_update_watermark(
        state=state,
        user_id=call.from_user.id,
        callback_data=callback_data,
    )
    await bot.edit_message_caption(
        chat_id=call.message.chat.id,
        caption=td.MM_POST,
        message_id=call.message.message_id,
        reply_markup=await ik.add_watermark(callback_data, data["Watermark"]),
    )


async def cant_more(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text="Нельзя выбрать более одного поля", show_alert=True)


async def delete_photo(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photo = data.get("photo")
    os.remove(path=photo)
    await state.update_data(photo="")
    await delete_logo_settings_user(call.message.chat.id)
    await photo_menu(call, state)
