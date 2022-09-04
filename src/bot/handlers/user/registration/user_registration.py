from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot, user_data
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.services.db.settings_user import create_settings_user
from bot.states import UserRegistration
from bot.services.db import user as user_db
from bot.utils.deleter import delete_user_message
from bot.utils.number_validator import is_phone_number_valid, is_email_valid
from bot.utils.state_worker import get_info_from_state

from bot_backend.models import User


async def start_client(call: types.CallbackQuery, state: FSMContext):
    await get_panel(call.message, state)


async def start_register_client(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    action = callback_data["action"]
    user_id = call.message.chat.id
    data = await state.get_data()
    mes_id = data.get("main_menu")
    if action == "1":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=mes_id,
            text=td.GET_NAME,
        )
        await UserRegistration.name.set()
    elif action == "2":
        await bot.edit_message_text(
            chat_id=user_id, message_id=mes_id, text=td.GET_NUMBER
        )
        await UserRegistration.number.set()
    else:
        await state.finish()
        await confirm_data(call, state)


async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    valid = await is_phone_number_valid(phone_number)
    if valid:
        await state.update_data(number=phone_number)
        await delete_user_message(message=message)
        await get_panel(message, state)
    else:
        data = await state.get_data()
        mes_id = data.get("main_menu")
        await bot.delete_message(message.chat.id, mes_id)
        mes = await bot.send_message(
            message.chat.id, "Введите номер телефона в формате 89999999999"
        )
        await delete_user_message(message)
        await state.update_data({"main_menu": mes.message_id})


async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await delete_user_message(message=message)
    await get_panel(message, state)


async def get_panel(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    nickname = message.chat.first_name
    data = await state.get_data()
    mes_id = data.get("main_menu")
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=mes_id,
        text=td.CLIENT_REG_MENU.format(
            nickname=nickname,
            name=await get_info_from_state(data, key="name"),
            number=await get_info_from_state(data, key="number"),
        ),
        reply_markup=await ik.setup_client(data),
    )
    await UserRegistration.registration.set()


async def confirm_data(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    nickname = call.message.chat.first_name
    data = await state.get_data()
    print(data.get("name"))
    name = await get_info_from_state(data, key="name")
    number = await get_info_from_state(data, key="number")
    print(name, number)
    await user_db.create_user(
        user_id=user_id,
        nickname=nickname,
        name=name,
        number=number,
    )
    await client_act_menu(call=call)


async def client_act_menu(call: types.CallbackQuery):
    user_id = call.message.chat.id
    await create_settings_user(user_id)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="""1. Для настройки анонсов зайдите в пункт меню НАСТРОЙКИ
2. В пункте ПРИВЕТСТВИЯ собраны приветствия, которые можно отправить клиентам в начале дня
3. В пункте ШАБЛОНЫ есть возможность сформировать индивидуальные настройки под каждый магазин
4. В пункте АНОНСЫ представлены анонсы, которые после настройки можно отправить клиентам""",
        reply_markup=await ik.get_main_menu(),
    )
