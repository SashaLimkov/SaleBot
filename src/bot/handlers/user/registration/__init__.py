from aiogram import Dispatcher
from aiogram.dispatcher import filters

from . import user_registration
from bot.states import UserRegistration
from bot.data import callback_data as cd


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        user_registration.start_client, filters.Text("registration"), state="*"
    )
    dp.register_callback_query_handler(
        user_registration.start_register_client,
        cd.reg.filter(),
        state=UserRegistration.registration,
    )
    dp.register_message_handler(user_registration.get_name, state=UserRegistration.name)
    dp.register_message_handler(
        user_registration.get_phone_number, state=UserRegistration.number
    )
