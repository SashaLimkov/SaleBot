from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from admin_bot.config.loader import bot
from admin_bot.states import PostAdding
from admin_bot.utils.deleter import delete_user_message
from admin_bot.utils.state_worker import get_info_from_state


async def start_add(call: types.CallbackQuery, state: FSMContext):
    await get_panel(call.message, state)


async def start_adding_post(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    action = callback_data["action"]
    data = await state.get_data()
    mes_id = data.get("main_menu")
    user_id = call.message.chat.id
    if action == "1":
        await bot.edit_message_text(
            chat_id=user_id, message_id=mes_id, text="Пришлите фото"
        )
        await PostAdding.album.set()
    else:
        await state.reset_state(with_data=False)
        await confirm_data(call, state)


async def get_photo_or_album(
    message: types.Message, album: List[types.Message], state: FSMContext
):
    # if valid:
    await state.update_data({"album": album})
    await delete_user_message(message=message)
    await get_panel(message, state)
    # else:
    #     data = await state.get_data()
    #     mes_id = data.get("main_menu")
    #     await bot.delete_message(
    #         message.chat.id,
    #         mes_id
    #     )
    #     mes = await bot.send_message(
    #         message.chat.id,
    #         "Введите номер телефона в формате 89999999999"
    #     )
    #     await delete_user_message(message)
    #     await state.update_data({"main_menu": mes.message_id})


async def get_panel(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    data = await state.get_data()
    name = message.chat.first_name
    mes_id = data.get("main_menu")
    album = await get_info_from_state(data, key="album")
    if album:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=mes_id,
            )
            media_group = types.MediaGroup()
            for obj in album:
                if obj.photo:
                    file_id = obj.photo[-1].file_id
                else:
                    file_id = obj[obj.content_type].file_id

                try:
                    # We can also add a caption to each file by specifying `"caption": "text"`
                    media_group.attach(
                        {
                            "media": file_id,
                            "type": obj.content_type,
                            "caption": obj.caption,
                        }
                    )
                except ValueError:
                    return await message.answer(
                        "This type of album is not supported by aiogram."
                    )

            await bot.send_media_group(
                chat_id=message.chat.id,
                media_group=media_group,
            )
        except:
            pass
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=mes_id,
        text="Чтобы продолжить заполните данные",
        # reply_markup=await ik.setup_client(data)
    )
    await PostAdding.adding.set()


async def confirm_data(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    data = await state.get_data()
    phone_number = await get_info_from_state(data, "phone_number")
    name = call.message.chat.first_name
    # await user_db.create_user(chat_id=user_id, phone_number=phone_number, name=name)
    # await user_menu(call.message, state)
