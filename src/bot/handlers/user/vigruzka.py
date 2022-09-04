from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.services.db.user import get_channels
from bot.keyboards import inline as ik


async def telegram(call: types.CallbackQuery, state: FSMContext):
    channels = await get_channels(call.message.chat.id)
    ch = "\n".join(channel.name_channel for channel in channels)
    text = f"Ваши каналы:\n{ch if ch else 'Пока нет каналов, не хотите добавить?'}"
    await bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=await ik.add_telegram_channel(),
    )
