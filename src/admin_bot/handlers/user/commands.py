from aiogram import types
from aiogram.dispatcher import FSMContext

from admin_bot.config.loader import bot
from admin_bot.keyboards import inline as ik


async def start_cmd(message: types.Message, state: FSMContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Выберите день",
        reply_markup=await ik.get_days()
    )


async def error(update: types.Update, exception):
    print(exception)
    r = update.get_current()
    try:
        chat_id = r.callback_query.from_user.id
    except:
        chat_id = r.message.from_user.id
    await bot.send_message(
        chat_id=chat_id,
        text="Напишите /start"
    )
    return
