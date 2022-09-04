from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.data import text_data as td
from bot.data.dict_data import MAIN_SETTINGS_SEGREGATOR
from bot.keyboards import inline as ik
from bot.services.db.settings_user import (
    update_formula_settings_user,
    get_formula_settings_user,
    get_formula_by_id_settings_user,
    update_commission_settings_user,
    get_commission_settings_user,
)
from bot.states.description import AddData, BaseState
from bot.utils import deleter
from bot.utils.is_float import is_float_number


async def change_c(call: types.CallbackQuery):
    await AddData.CHANGE_C.set()
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text="Введите свой коэффециент для С",
        message_id=call.message.message_id,
    )


async def set_c(message: types.Message, state: FSMContext):
    data = await state.get_data()
    c = message.text
    chat_id = message.chat.id
    m_mes = data.get("main_menu")
    if await is_float_number(c):
        await deleter.delete_user_message(message)
        await deleter.delete_mes(chat_id, m_mes)
        await update_commission_settings_user(chat_id, round(float(c), 2))
        selected = await get_formula_settings_user(chat_id)
        mes = await bot.send_message(
            chat_id=chat_id,
            text=td.MM_FORMULA.format(
                selected=selected if selected else "отсутствует",
                formula="100$(A) - 30%(B) + 10%(C) = 77$",
                com=await get_commission_settings_user(chat_id),
            ),
            reply_markup=await ik.formula({"action": 1, "settings": 2}),
        )
        await state.update_data(main_menu=mes.message_id)
        await BaseState.BASE.set()
    else:
        await deleter.delete_user_message(message)
        try:
            await bot.edit_message_text(
                chat_id=chat_id, message_id=m_mes, text="Введите число"
            )
        except:
            pass


async def select_formula(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    chat_id = call.message.chat.id
    page = callback_data["select"]
    selected = await get_formula_settings_user(chat_id)
    formula = await get_formula_by_id_settings_user(page)
    await update_formula_settings_user(call.from_user.id, int(page))
    await call.answer(text="Выбранная формула обновлена")
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            text=td.MM_FORMULA.format(
                selected=selected if selected else "отсутствует",
                formula=formula,
                com=await get_commission_settings_user(chat_id),
            ),
            message_id=call.message.message_id,
            reply_markup=await ik.formula(callback_data),
        )
    except:
        pass


async def formula_pag(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    chat_id = call.message.chat.id
    page = callback_data["page"]
    selected = await get_formula_settings_user(chat_id)
    formula = await get_formula_by_id_settings_user(page)
    await bot.edit_message_text(
        chat_id=chat_id,
        text=td.MM_FORMULA.format(
            selected=selected if selected else "отсутствует",
            formula=formula,
            com=await get_commission_settings_user(chat_id),
        ),
        message_id=call.message.message_id,
        reply_markup=await ik.formula(callback_data),
    )
