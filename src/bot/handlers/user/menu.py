from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import deep_linking
from aiogram.utils.markdown import hcode

from admin_bot.services.db.posts import get_user
from bot.config.loader import bot
from bot.data import text_data as td
from bot.data.dict_data import MAIN_SETTINGS_SEGREGATOR
from bot.keyboards import inline as ik
from bot.services.db.settings_user import (
    get_signature_settings_user,
    get_formula_settings_user,
    get_currency_settings_user,
    get_commission_settings_user,
)
from bot.states.anons import Anons
from bot.states.description import BaseState
from bot.utils import deleter
from bot.utils.state_worker import state_update_fields
from bot_backend.models import User


async def get_mm(call: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=td.MM_TEXT,
        message_id=call.message.message_id,
        reply_markup=await ik.get_main_menu(),
    )


async def anons(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=td.MM_ANONS,
        reply_markup=await ik.get_anons(),
    )


async def anons_set(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(anons_date=call.data.split("_")[-1])
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Вернуться в чат", switch_inline_query=""))
    await call.message.edit_text("Дата анонса успешно установлена", reply_markup=kb)
    await Anons.ANONS.set()


async def main_segragator(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await BaseState.BASE.set()
    action = callback_data["action"]
    action = int(action)
    if action == 1:
        try:
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=td.MM_PSBT,
                message_id=call.message.message_id,
                reply_markup=await ik.get_settings(callback_data),
            )
        except:
            await deleter.delete_mes(call.message.chat.id, call.message.message_id)
            mes = await bot.send_message(
                chat_id=call.message.chat.id,
                text=td.MM_PSBT,
                reply_markup=await ik.get_settings(callback_data),
            )
            await state.update_data(main_menu=mes.message_id)

    elif action == 2:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=td.MM_ANONS,
            message_id=call.message.message_id,
            reply_markup=await ik.get_anons(),
        )
    elif action == 3:
        pass
    elif action == 4:
        pass
    else:
        pass


async def main_settings_segregator(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    action = callback_data["settings"]
    action = int(action)
    data = await state.get_data()
    mes_id = call.message.message_id
    chat_id = call.message.chat.id
    d_data = MAIN_SETTINGS_SEGREGATOR[action]
    tg_user: User = await get_user(user_id=chat_id)
    print(tg_user.number)
    if action == 1:
        selected = await get_currency_settings_user(chat_id)
        await bot.edit_message_text(
            chat_id=chat_id,
            text=d_data[0].format(cur=selected),
            message_id=mes_id,
            reply_markup=await ik.select_cur(callback_data),
        )
    elif action == 2:
        selected = await get_formula_settings_user(chat_id)
        await bot.edit_message_text(
            chat_id=chat_id,
            text=d_data[0].format(
                selected=selected if selected else "отсутствует",
                formula="100$(A) - 30%(B) + 10%(C) = 77$",
                com=await get_commission_settings_user(chat_id),
            ),
            message_id=mes_id,
            reply_markup=await ik.formula(callback_data),
        )
    elif action == 3:
        is_photo = data.get("photo", False)
        print(is_photo)
        if is_photo:
            await deleter.delete_mes(chat_id, mes_id)
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
        else:
            await bot.edit_message_text(
                chat_id=chat_id,
                text=d_data[0] if is_photo else td.MM_ADD_PHOTO,
                message_id=mes_id,
                reply_markup=await ik.add_photo(
                    callback_data,
                    data["Watermark"] if "Watermark" in data else [],
                    is_photo,
                ),
            )

    elif action == 4:
        await bot.edit_message_text(
            chat_id=chat_id,
            text=d_data[0],
            message_id=mes_id,
            reply_markup=await ik.info_on_off(
                callback_data, data["Fields"] if "Fields" in data else []
            ),
        )
    elif action == 5:
        sign = await get_signature_settings_user(
            chat_id,
        )
        await bot.edit_message_text(
            chat_id=chat_id,
            text=d_data[0].format(sign=sign if sign else "отсутствует"),
            message_id=mes_id,
            reply_markup=await ik.signature(callback_data, user_id=chat_id),
        )
    elif action == 6:
        await bot.edit_message_text(
            chat_id=chat_id,
            text=d_data[0],
            message_id=mes_id,
            reply_markup=await ik.short_link(
                callback_data, data["Link"] if "Link" in data else False
            ),
        )
    elif action == 7:
        await bot.edit_message_text(
            chat_id=chat_id,
            text=d_data[0],
            message_id=mes_id,
            reply_markup=await ik.vigruzka(),
        )
    elif action == 8:
        share_link = await deep_linking.get_start_link(
            f"{call.message.chat.id}", encode=True
        )
        user = await get_user(chat_id)
        count_of = user.count_members
        await bot.edit_message_text(
            chat_id=chat_id,
            text=d_data[0].format(count=count_of, link=hcode(share_link)),
            message_id=mes_id,
            reply_markup=await ik.back_to(),
        )
    else:
        await bot.edit_message_text(
            chat_id=chat_id,
            text=d_data[0],
            message_id=mes_id,
            reply_markup=await ik.second_action(
                callback_data=callback_data, row_width=d_data[1], buttons=d_data[2]
            ),
        )


async def select_field(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state_update_fields(
        state=state,
        user_id=call.from_user.id,
        key=True,
        callback_data=callback_data,
        add_data=True,
    )
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=td.MM_INFO,
        message_id=call.message.message_id,
        reply_markup=await ik.info_on_off(callback_data, data["Fields"]),
    )


async def cancel_selection_field(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state_update_fields(
        state=state,
        user_id=call.from_user.id,
        key=False,
        callback_data=callback_data,
    )
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=td.MM_INFO,
        message_id=call.message.message_id,
        reply_markup=await ik.info_on_off(callback_data, data["Fields"]),
    )
