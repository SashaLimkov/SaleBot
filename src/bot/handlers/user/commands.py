from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import deep_linking

from bot.config.loader import bot
from bot.keyboards import inline as ik
from bot.services.db import user as user_db
from bot.services.db.user import create_member, get_user
from bot.utils import deleter


async def start_cmd(message: types.Message, state: FSMContext):
    user = await user_db.get_user(message.chat.id)
    try:
        data = await state.get_data()
        await bot.delete_message(
            chat_id=message.chat.id, message_id=data.get("main_menu")
        )
    except:
        pass
    args = message.get_args()
    if args:
        info = deep_linking.decode_payload(args)
        print(info)
        user = await get_user(int(info))
        if user.count_members < 3:
            await create_member(message.from_user.id, int(info))
        else:
            await message.answer(
                "Ничего не вышло, количество переходов по ссылке превышено"
            )
            return
    if not user:
        mes = await bot.send_message(
            chat_id=message.chat.id,
            text="Чтобы продолжить надо пройти регистрацию",
            reply_markup=await ik.reg_btn(),
        )
    else:
        mes = await bot.send_message(
            chat_id=message.chat.id,
            text="""1. Для настройки анонсов зайдите в пункт меню НАСТРОЙКИ
2. В пункте ПРИВЕТСТВИЯ собраны приветствия, которые можно отправить клиентам в начале дня
3. В пункте ШАБЛОНЫ есть возможность сформировать индивидуальные настройки под каждый магазин
4. В пункте АНОНСЫ представлены анонсы, которые после настройки можно отправить клиентам""",
            reply_markup=await ik.get_main_menu(),
        )

    await deleter.delete_mes(message.chat.id, message.message_id)
    await state.update_data({"main_menu": mes.message_id})


async def error(update: types.Update, exception):
    print(exception)
    # r = update.get_current()
    # try:
    #     chat_id = r.callback_query.from_user.id
    # except:
    #     chat_id = r.message.from_user.id
    # await bot.send_message(chat_id=chat_id, text="Напишите /start")
    return
