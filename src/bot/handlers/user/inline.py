from aiogram import types

from admin_bot.config.loader import bot
from bot import states, keyboards
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
)
import hashlib
import datetime
import requests

from bot.services.db.post import get_post_by_date_shop
from bot.services.db.settings_shop_user import get_settings_shop_user_by_user
from bot.services.db.settings_user import get_settings_user_by_user
from bot.services.db.shop import get_shops_name, get_shop_by_name, get_shops
from bot.services.db.user import delete_channel, create_channel, get_channels, get_user_channel
from bot.utils import deleter
from bot.utils.generate_watermark import watermark


async def sender_anons(message: types.Message, state: FSMContext):
    shop, date = message.text.split("|:|")
    try:
        await deleter.delete_user_message(message)
    except:
        pass
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    posts = await get_post_by_date_shop(date, shop)
    if message.chat.id < 0:
        chat_id = await get_user_channel(message.chat.id)
    else:
        chat_id = message.chat.id
    settings_user = await get_settings_shop_user_by_user(chat_id, shop)
    if not settings_user:
        settings_user = await get_settings_user_by_user(chat_id)

    shop_obj = await get_shop_by_name(shop)
    currency_shop = shop_obj.currency.currency
    course = requests.get("https://cdn.cur.su/api/cbr.json").json()
    course = (
        course["rates"][settings_user.currency.currency]
        / course["rates"][currency_shop]
    )

    for post, content in posts.items():
        try:
            media_group = types.MediaGroup()
            text_post = "<b>" + post.shop.name + "</b>\n\n"
            counter = 0
            for item in content["items"]:
                if settings_user.product.name:
                    text_post += item.name + "\n"
                if settings_user.product.description:
                    if item.description:
                        text_post += item.description + "\n"
                if settings_user.product.price:
                    price = item.cost
                    discount = price // 100 * item.discount
                    commisison = price // 100 * settings_user.commission
                    if settings_user.formula.name == "100$(A) - 30%(B) = 70$":
                        price = price - discount
                    elif (
                        settings_user.formula.name
                        == "100$(A) - (30%(B) - 10%(C)) = 80$"
                    ):
                        price = price - (discount - commisison)
                    elif (
                        settings_user.formula.name == "100$(A) - 30%(B) + 10%(C) = 77$"
                    ):
                        price = price - discount + commisison
                    price = round(price * course, 2)
                    if settings_user.product.discount:
                        text_post += f"<b>{price}{settings_user.currency.sign}</b> {item.discount}%\n"
                    else:
                        text_post += f"{price} {settings_user.currency.sign}\n"
                if settings_user.product.link:
                    if settings_user.link:
                        text_post += f'<a href="{item.link}">Ссылка</a>\n\n'
                    else:
                        text_post += f"{item.link}\n\n"
            if settings_user.signature:
                text_post += settings_user.signature
            for obj in content["images"]:
                if settings_user.logo:
                    if counter == 0:
                        file = types.InputMediaPhoto(
                            types.InputFile(
                                watermark(
                                    obj.image.path,
                                    settings_user.logo.path,
                                    settings_user.logo_position,
                                )
                            ),
                            caption=text_post,
                        )
                    else:
                        file = types.InputMediaPhoto(
                            types.InputFile(
                                watermark(
                                    obj.image.path,
                                    settings_user.logo.path,
                                    settings_user.logo_position,
                                )
                            )
                        )
                    media_group.attach_photo(photo=file)
                    counter += 1
                else:
                    if counter == 0:
                        file = types.InputMediaPhoto(
                            types.InputFile(obj.image.path), caption=text_post
                        )
                    else:
                        file = types.InputMediaPhoto(types.InputFile(obj.image.path))
                    media_group.attach_photo(photo=file)
                    counter += 1
            await message.answer_media_group(media=media_group)
        except:
            pass


async def inline_shops(inline_query: InlineQuery, state: FSMContext):
    state_data = await state.get_data()
    results = []
    if "anons_date" in state_data:
        if state_data["anons_date"]:
            date = datetime.datetime.strptime(state_data["anons_date"], "%Y-%m-%d")
            shops = {item.name: item for item in await get_shops()}
            shop_list = await get_shops_name()
            shop_list.sort()
            for index, shop in enumerate(shop_list):
                if await get_post_by_date_shop(date, shops[shop]):
                    result_id: str = hashlib.md5(str(index).encode()).hexdigest()
                    results.append(
                        InlineQueryResultArticle(
                            id=result_id,
                            title=shop,
                            input_message_content=InputTextMessageContent(
                                f'{shop}|:|{state_data["anons_date"]}'
                            ),
                        )
                    )
    switch_text = "Выбрать дату релиза >>"
    return await inline_query.answer(
        results,
        cache_time=0,
        is_personal=True,
        switch_pm_parameter="select_section",
        switch_pm_text=switch_text,
    )


async def inline_null(inline_query: InlineQuery, state: FSMContext):
    switch_text = "Выбрать дату релиза >>"
    return await inline_query.answer(
        [],
        cache_time=0,
        is_personal=True,
        switch_pm_parameter="select_section",
        switch_pm_text=switch_text,
    )


async def chanel_handler(message: types.Message):
    chanel_id = message.chat.id
    user_id = message.from_user.id
    if (
        message.new_chat_member.status == "left"
        or message.new_chat_member.status == "kicked"
    ):
        await delete_channel(chanel_id)
    else:
        await create_channel(user_id, chanel_id, message.chat.title)


async def inline_list_channels(inline_query: InlineQuery, state: FSMContext):
    results = []
    channels = get_channels(inline_query.from_user.id)
    for index, channel in enumerate(channels):
        result_id: str = hashlib.md5(str(index).encode()).hexdigest()
        results.append(
            InlineQueryResultArticle(
                id=result_id,
                title=channel.name + channel,
                input_message_content=InputTextMessageContent(f"{channel.chat_id}"),
            )
        )
    return await inline_query.answer(results, cache_time=0, is_personal=True)
