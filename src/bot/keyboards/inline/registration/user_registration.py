from aiogram.types import InlineKeyboardMarkup

from bot.data import callback_data as cd
from bot.data import list_data as ld
from bot.utils.butto_worker import add_button


async def setup_client(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for index, text in enumerate(ld.REG_CLIENT):
        keyboard.add(
            await add_button(
                text=text,
                cd=cd.reg.new(
                    action=index + 1
                ))
        )
    if "name" in data and "second_name" in data and "number" in data and "email" in data and "city" in data:
        keyboard.add(
            await add_button(
                text="Подтвердить данные",
                cd=cd.reg.new(
                    action="submit"
                )
            )
        )
    return keyboard

async def reg_btn():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        await add_button(
            text="Зарегистрироваться",
            cd="registration"
        )
    )
    return keyboard