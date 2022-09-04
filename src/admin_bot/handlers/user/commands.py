from aiogram import types
from aiogram.dispatcher import FSMContext

from admin_bot.config.loader import bot
from admin_bot.keyboards import inline as ik


async def main_menu(call: types.CallbackQuery, state: FSMContext):
    await start_cmd(call.message, state)


async def start_cmd(message: types.Message, state: FSMContext):
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            text=f"Выберите день",
            message_id=message.message_id,
            reply_markup=await ik.get_days(),
        )
    except:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Выберите день",
            reply_markup=await ik.get_days(),
        )


async def error(update: types.Update, exception):
    print(exception)
    r = update.get_current()
    try:
        chat_id = r.callback_query.from_user.id
    except:
        chat_id = r.message.from_user.id
    await bot.send_message(chat_id=chat_id, text="Напишите /start")
    return
