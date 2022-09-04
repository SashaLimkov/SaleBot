from aiogram.dispatcher import FSMContext

from bot.data.dict_data import INFO_SAVER
from bot.services.db.settings_user import (
    update_link_settings_user,
    update_logo_settings_user,
    update_logo_position_settings_user,
)


async def get_info_from_state(data, key):
    return data[key] if key in list(data.keys()) else ""


async def state_update_fields(
    state: FSMContext,
    user_id: int,
    key: bool,
    callback_data: dict,
    add_data: bool = False,
):
    data = await state.get_data()
    await add_data_to_data(data, add_data, callback_data, state, "Fields")
    await INFO_SAVER[int(callback_data["field"])](user_id, key)
    return data


async def state_update_watermark(
    state: FSMContext,
    user_id: int,
    callback_data: dict,
    add_data: bool = False,
):
    data = await state.get_data()
    await add_data_to_data(data, add_data, callback_data, state, "Watermark")
    path = data.get("photo")
    position = data.get("Watermark")
    await update_logo_position_settings_user(user_id, position[0] if position else [])
    await update_logo_settings_user(user_id, path)
    return data


async def short_link_worker(
    state: FSMContext, user_id: int, callback_data: dict, add_data: bool = False
):
    data = await state.get_data()
    if add_data:
        if "Link" not in data:
            data["Link"] = callback_data["field"]
    data["Link"] = callback_data["field"]
    await state.update_data({"Link": data["Link"]})
    await update_link_settings_user(user_id, callback_data["field"])
    return data


async def add_data_to_data(data, add_data, callback_data, state, key):
    if add_data:
        if key in data:
            data[key].append(callback_data["field"])
        else:
            data[key] = [callback_data["field"]]
    else:
        data[key].remove(callback_data["field"])
    await state.update_data({key: data[key]})
    return data
