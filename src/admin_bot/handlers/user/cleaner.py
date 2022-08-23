from typing import List

from aiogram import types


async def clean_s(message: types.Message, album: List[types.Message]):
    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type, "caption": obj.caption})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")

    await message.answer_media_group(media_group)
    # await bot.delete_message(
    #     chat_id=message.from_user.id, message_id=message.message_id
    # )
