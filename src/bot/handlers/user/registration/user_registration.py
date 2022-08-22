from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot, user_data
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.states import UserRegistration
from bot.services.db import user as user_db
from bot.utils.deleter import delete_user_message
from bot.utils.number_validator import is_phone_number_valid, is_email_valid
from bot.utils.state_worker import get_info_from_state

from bot_backend.models import User


async def start_client(call: types.CallbackQuery, state: FSMContext):
    await get_panel(call.message, state)


async def start_register_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    user_id = call.message.chat.id
    data = await state.get_data()
    mes_id = data.get("main_menu")
    print(1)
    if action == "1":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=mes_id,
            text=td.GET_NAME,
        )
        await UserRegistration.name.set()
    elif action == "2":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=mes_id,
            text=td.GET_SECOND_NAME
        )
        await UserRegistration.second_name.set()

    elif action == "3":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=mes_id,
            text=td.GET_EMAIL
        )
        await UserRegistration.email.set()

    elif action == "4":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=mes_id,
            text=td.GET_NUMBER
        )
        await UserRegistration.number.set()
    elif action == "5":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=mes_id,
            text=td.GET_CITY
        )
        await UserRegistration.city.set()
    else:
        await state.finish()
        await confirm_data(call, state)


async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    valid = await is_phone_number_valid(phone_number)
    if valid:
        await state.update_data({"number": phone_number})
        await delete_user_message(message=message)
        await get_panel(message, state)
    else:
        data = await state.get_data()
        mes_id = data.get("main_menu")
        await bot.delete_message(
            message.chat.id,
            mes_id
        )
        mes = await bot.send_message(
            message.chat.id,
            "Введите номер телефона в формате 89999999999"
        )
        await delete_user_message(message)
        await state.update_data({"main_menu": mes.message_id})


async def get_email(message: types.Message, state: FSMContext):
    email = message.text
    valid = await is_email_valid(email)
    if valid:
        await state.update_data({"email": email})
        await delete_user_message(message=message)
        await get_panel(message, state)
    else:
        data = await state.get_data()
        mes_id = data.get("main_menu")
        await bot.delete_message(
            message.chat.id,
            mes_id
        )
        mes = await bot.send_message(
            message.chat.id,
            "Введите корректную почту формата foo@foo.foo"
        )
        await delete_user_message(message)
        await state.update_data({"main_menu": mes.message_id})


async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})
    await delete_user_message(message=message)
    await get_panel(message, state)


async def get_second_name(message: types.Message, state: FSMContext):
    second_name = message.text
    await state.update_data({"second_name": second_name})
    await delete_user_message(message=message)
    await get_panel(message, state)


async def get_city(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data({"city": city})
    await delete_user_message(message=message)
    await get_panel(message, state)


async def get_panel(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    nickname = message.chat.first_name
    data = await state.get_data()
    mes_id = data.get('main_menu')
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=mes_id,
        text=td.CLIENT_REG_MENU.format(
            nickname=nickname,
            name=await get_info_from_state(data, key="name"),
            second_name=await get_info_from_state(data, key="second_name"),
            number=await get_info_from_state(data, key="number"),
            email=await get_info_from_state(data, key="email"),
            city=await get_info_from_state(data, key="city"),
        ),
        reply_markup=await ik.setup_client(data)
    )
    await UserRegistration.registration.set()


async def confirm_data(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    nickname = call.message.chat.first_name
    data = await state.get_data()
    name = await get_info_from_state(data, key="name")
    second_name = await get_info_from_state(data, key="second_name")
    number = await get_info_from_state(data, key="number")
    email = await get_info_from_state(data, key="email")
    city = await get_info_from_state(data, key="city")

    await user_db.create_user(user_id=user_id, nickname=nickname, name=name, second_name=second_name, number=number,
                              email=email, city=city)
    await client_act_menu(call=call)


async def client_act_menu(call: types.CallbackQuery):
    user_id = call.message.chat.id
    tg_user: User = await user_db.get_user(user_id=user_id)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text="Вы зарегестрированы"
    )
