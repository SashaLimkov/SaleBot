from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.data import callback_data as cd
from bot.data import list_data as ld
from bot.services.db.currency import get_currency
from bot.services.db.settings_user import get_signature_settings_user
from bot.utils.butto_worker import add_button


async def get_settings(callback_data: dict):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for index, text in enumerate(ld.MM_SETTINGS):
        keyboard.insert(
            await add_button(
                text=text,
                cd=cd.mm_settings.new(
                    action=callback_data["action"],
                    settings=index + 1,
                ),
            )
        )
    keyboard.add(await add_button(text="Назад", cd="back"))
    return keyboard


async def second_action(callback_data: dict, row_width=1, buttons: list = None):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    for index, text in enumerate(buttons):
        keyboard.insert(
            await add_button(
                text=text,
                cd=cd.mm_settings_act.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    act2=index + 1,
                ),
            )
        )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=callback_data["action"],
            ),
        )
    )
    return keyboard


async def get_currency_change(callback_data: dict):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for index, text in enumerate(ld.MM_S_CUR_CHANGE):
        keyboard.insert(
            await add_button(
                text=text,
                cd=cd.mm_s_cur_ch.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    act2=callback_data["act2"],
                    change=index + 1,
                ),
            )
        )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm_settings_act.new(
                action=callback_data["action"],
                settings=callback_data["settings"],
                act2=callback_data["act2"],
            ),
        )
    )
    return keyboard


async def info_on_off(callback_data: dict, selected_fields: list):
    keyboard = InlineKeyboardMarkup(row_width=1)
    fields = [
        ["Ссылка", 1],
        ["Название", 2],
        ["Цена", 3],
        ["Скидка", 4],
        ["Описание", 5],
    ]  # db.get_fields()
    for field in fields:
        if str(field[1]) in selected_fields:
            keyboard.insert(
                await add_button(
                    text=f"✅ {field[0]}",
                    cd=cd.mm_s_info_c.new(
                        action=callback_data["action"],
                        settings=callback_data["settings"],
                        field=field[1],
                    ),
                )
            )
        else:
            keyboard.insert(
                await add_button(
                    text=f"⬜ {field[0]}",
                    cd=cd.mm_s_info.new(
                        action=callback_data["action"],
                        settings=callback_data["settings"],
                        field=field[1],
                    ),
                )
            )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=callback_data["action"],
            ),
        )
    )
    return keyboard


async def short_link(callback_data: dict, is_short):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if is_short == "True":
        keyboard.insert(
            await add_button(
                text=f"✅ Короткая ссылка",
                cd=cd.mm_l_link.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    field=False,
                ),
            )
        )
    else:
        keyboard.insert(
            await add_button(
                text=f"⬜ Короткая ссылка",
                cd=cd.mm_s_link.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    field=True,
                ),
            )
        )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=callback_data["action"],
            ),
        )
    )
    return keyboard


async def signature(callback_data: dict, user_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        await add_button(
            text="Изменить",
            cd=cd.mm_signature.new(
                action=callback_data["action"],
                settings=callback_data["settings"],
                act="1",
            ),
        )
    )
    sign = await get_signature_settings_user(user_id)
    print(sign)
    if sign:
        keyboard.add(
            await add_button(
                text="Удалить",
                cd=cd.mm_signature.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    act="2",
                ),
            )
        )

    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=callback_data["action"],
            ),
        )
    )
    return keyboard


async def formula(callback_data: dict):
    keyboard = InlineKeyboardMarkup(row_width=2)
    if "page" not in callback_data:
        page = 0
    else:
        page = int(callback_data["page"])
    if int(page) > 0:
        keyboard.insert(
            await add_button(
                text="◀",
                cd=cd.mm_formula.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    page=page - 1,
                ),
            )
        )
    if int(page) < 2:
        keyboard.insert(
            await add_button(
                text="▶",
                cd=cd.mm_formula.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    page=page + 1,
                ),
            )
        )
    keyboard.add(
        await add_button(
            text=f"Выбрать формулу {page+1}",
            cd=cd.mm_formula_select.new(
                action=callback_data["action"],
                settings=callback_data["settings"],
                select=page,
            ),
        )
    )
    keyboard.add(
        await add_button(text=f"Изменить C", cd="change_c"),
    )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=callback_data["action"],
            ),
        )
    )
    return keyboard


async def select_cur(callback_data: dict):
    keyboard = InlineKeyboardMarkup(row_width=3)
    cur_list = await get_currency()
    for cur in cur_list:
        keyboard.insert(
            await add_button(
                text=cur,
                cd=cd.mm_cur.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    cur=cur,
                ),
            )
        )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=callback_data["action"],
            ),
        )
    )
    return keyboard


async def add_watermark(callback_data: dict, selected_fields: list):
    keyboard = InlineKeyboardMarkup(row_width=2)
    fields = [
        ["Левый верхний угол", 1],
        ["Правый верхний угол", 2],
        ["Левый нижний угол", 3],
        ["Правый нижний угол", 4],
    ]
    zz = {
        "1": "Левый верхний угол",
        "2": "Правый верхний угол",
        "3": "Левый нижний угол",
        "4": "Правый нижний угол",
    }
    if not selected_fields:
        for key, value in zz.items():
            if key in selected_fields:
                keyboard.insert(
                    await add_button(
                        text=f"✅ {value}",
                        cd=cd.mm_post_c.new(
                            action=callback_data["action"],
                            settings=callback_data["settings"],
                            field=key,
                        ),
                    )
                )
            else:
                keyboard.insert(
                    await add_button(
                        text=f"⬜ {value}",
                        cd=cd.mm_post.new(
                            action=callback_data["action"],
                            settings=callback_data["settings"],
                            field=key,
                        ),
                    )
                )
    else:
        for key, value in zz.items():
            if key in selected_fields:
                keyboard.insert(
                    await add_button(
                        text=f"✅ {value}",
                        cd=cd.mm_post_c.new(
                            action=callback_data["action"],
                            settings=callback_data["settings"],
                            field=key,
                        ),
                    )
                )
            else:
                keyboard.insert(await add_button(text=f"❌ {value}", cd="cant_more"))
    # for field in fields:
    #     if str(field[1]) in selected_fields:
    #         keyboard.insert(
    #             await add_button(
    #                 text=f"✅ {field[0]}",
    #                 cd=cd.mm_post_c.new(
    #                     action=callback_data["action"],
    #                     settings=callback_data["settings"],
    #                     field=field[1],
    #                 ),
    #             )
    #         )
    #     else:
    #         keyboard.insert(
    #             await add_button(
    #                 text=f"⬜ {field[0]}",
    #                 cd=cd.mm_post.new(
    #                     action=callback_data["action"],
    #                     settings=callback_data["settings"],
    #                     field=field[1],
    #                 ),
    #             )
    #         )
    keyboard.add(
        await add_button(
            text="Удалить фото",
            cd="delete_photo",
        )
    )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=callback_data["action"],
            ),
        )
    )
    return keyboard


async def add_photo(callback_data: dict, selected_fields: list, is_photo):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if is_photo:
        keyboard = await add_watermark(callback_data, selected_fields)
    else:
        keyboard.add(
            await add_button(
                text="Добавить фото",
                cd=cd.mm_add_photo.new(
                    action=callback_data["action"],
                    settings=callback_data["settings"],
                    add=1,
                ),
            )
        )
        keyboard.add(
            await add_button(
                text="Назад",
                cd=cd.mm.new(
                    action=callback_data["action"],
                ),
            )
        )
    return keyboard


async def save_photo():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(await add_button(text="Сохранить фото", cd="save_photo"))
    keyboard.add(await add_button(text="Назад", cd="back_to_s_m"))
    return keyboard


async def vigruzka():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(await add_button(text="Telegram", cd="telegram_btn"))
    keyboard.add(await add_button(text="Viber", cd="Viber_btn"))
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm.new(
                action=1,
            ),
        )
    )
    return keyboard


async def add_telegram_channel():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Добавить канал", switch_inline_query=""))
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.mm_settings.new(
                action=1,
                settings=7,
            ),
        )
    )
    return keyboard
