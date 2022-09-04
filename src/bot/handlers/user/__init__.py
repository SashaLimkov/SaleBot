from aiogram import Dispatcher, types
from aiogram.dispatcher import filters

from bot.handlers.user import (
    cleaner,
    registration,
    commands,
    menu,
    description,
    link,
    formula,
    currency,
    post,
    inline,
    vigruzka,
)
from bot.states.anons import Anons
from bot.states.description import AddData, BaseState
from bot.middleware import AlbumMiddleware
from bot.data import callback_data as cd


def setup(dp: Dispatcher):
    dp.middleware.setup(AlbumMiddleware())
    dp.register_errors_handler(commands.error)
    dp.register_inline_handler(inline.inline_shops, state=Anons.ANONS)
    dp.register_inline_handler(inline.inline_null, state="*")
    dp.register_message_handler(
        inline.sender_anons, filters.Text(contains="|:|"), state="*"
    )
    dp.register_my_chat_member_handler(inline.chanel_handler, state="*")
    dp.register_channel_post_handler(
        inline.sender_anons, filters.Text(contains="|:|"), state="*"
    )
    dp.register_message_handler(
        menu.anons, filters.CommandStart(deep_link="select_section"), state="*"
    )
    dp.register_message_handler(commands.start_cmd, filters.CommandStart(), state="*")
    registration.setup(dp)
    dp.register_callback_query_handler(menu.main_segragator, cd.mm.filter(), state="*")
    dp.register_callback_query_handler(
        menu.anons_set, filters.Text(startswith="day"), state="*"
    )
    dp.register_callback_query_handler(
        menu.main_settings_segregator, cd.mm_settings.filter(), state="*"
    )
    dp.register_callback_query_handler(
        currency.select_cur, cd.mm_cur.filter(), state="*"
    )
    dp.register_callback_query_handler(
        formula.select_formula, cd.mm_formula_select.filter(), state="*"
    )
    dp.register_callback_query_handler(
        formula.formula_pag, cd.mm_formula.filter(), state="*"
    )

    dp.register_callback_query_handler(
        menu.select_field, cd.mm_s_info.filter(), state="*"
    )
    dp.register_callback_query_handler(
        link.short_link, cd.mm_s_link.filter(), state="*"
    )
    dp.register_callback_query_handler(
        link.cancel_short_link, cd.mm_l_link.filter(), state="*"
    )
    dp.register_callback_query_handler(
        description.description_settings, cd.mm_signature.filter(), state="*"
    )
    dp.register_message_handler(description.set_description, state=AddData.INPUT)
    dp.register_callback_query_handler(
        menu.cancel_selection_field, cd.mm_s_info_c.filter(), state="*"
    )
    dp.register_callback_query_handler(menu.get_mm, filters.Text("back"), state="*")
    dp.register_callback_query_handler(
        post.select_watermark, cd.mm_post.filter(), state="*"
    )
    dp.register_callback_query_handler(
        post.cancel_selection_watermark, cd.mm_post_c.filter(), state="*"
    )
    dp.register_callback_query_handler(
        post.add_photo, cd.mm_add_photo.filter(), state="*"
    )
    dp.register_message_handler(
        post.photo_keeper,
        content_types=types.ContentType.ANY,
        state=AddData.ADD_DOCUMENT,
    )
    dp.register_callback_query_handler(
        post.photo_menu, filters.Text("back_to_s_m"), state="*"
    )
    dp.register_callback_query_handler(
        post.save_photo, filters.Text("save_photo"), state="*"
    )
    dp.register_callback_query_handler(
        post.cant_more, filters.Text("cant_more"), state="*"
    )
    dp.register_callback_query_handler(
        post.delete_photo, filters.Text("delete_photo"), state="*"
    )
    dp.register_callback_query_handler(
        formula.change_c, filters.Text("change_c"), state="*"
    )
    dp.register_message_handler(formula.set_c, state=AddData.CHANGE_C)
    dp.register_callback_query_handler(
        vigruzka.telegram, filters.Text("telegram_btn"), state="*"
    )
    dp.register_message_handler(
        cleaner.clean_s,
        is_media_group=True,
        content_types=types.ContentType.ANY,
        state="*",
    )
