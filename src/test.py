import configparser
import json
import random
import re

from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime
import telethon

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, MessageMediaPhoto

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
import django, os
from django.core.files import File

api_id = 6168039
api_hash = "cc6dc8f166a93a75c0275293d120f3e8"
username = "jif_jif"

client = TelegramClient(username, api_id, api_hash)
client.start()


async def dump_all_messages(channel):
    from bot_backend.models import Post, Item, Image, Shop, Currency

    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 5  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 5  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        """Класс для сериализации записи дат в JSON"""

        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(
            GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None,
                add_offset=0,
                limit=limit_msg,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            try:
                if type(message.media) == MessageMediaPhoto:
                    pass
                    # await client.download_media(message.media, message.file.name)

                text = message.message

                name_shop = text.split("\n")[0][:-2]
                if "Находка дня" in name_shop:
                    name_shop = text.split("\n")[1][:-2]
                data = text.split("\n\n")
                data[0] = "\n".join(data[0].split("\n")[1:])
                pattern = r"(?P<url>https?://[^\s]+)"
                flag = False
                for item in name_shop:
                    if item in "ёйцукенгшщзхъфывапролджэячсмитьбю":
                        flag = True
                        break
                list_products = []
                try:
                    if not flag:
                        res_1 = re.findall(pattern, message.message)
                        res = re.findall(
                            r"([$€]\d*\.\d+|\d+\.\d*[$€]|[$€]\d*|\d+[$€])",
                            message.message,
                        )
                        if (
                            res
                            and res_1
                            and name_shop
                            and res[0] != "$"
                            and res[0] != "€"
                        ):
                            for index, item in enumerate(data):
                                item = item.split("\n")
                                descr = ""
                                if "$" in item[0] or "€" in item[0]:
                                    name = item[0].split("➡")[0]
                                    for item_2 in item[1:]:
                                        if "http" in item_2:
                                            pass
                                        else:
                                            descr += "\n" + item_2
                                elif "Находка дня" in item[0]:
                                    name = item[1]
                                    descr = ""
                                    for item_2 in item[3:]:
                                        if "http" in item_2:
                                            pass
                                        else:
                                            descr += "\n" + item_2
                                else:
                                    name = item[0]
                                    descr = ""
                                    for item_2 in item[2:]:
                                        if "http" in item_2:
                                            pass
                                        else:
                                            descr += "\n" + item_2
                                list_products.append(
                                    {
                                        "name": name,
                                        "price": res[index],
                                        "descr": descr,
                                        "link": res_1[index],
                                    }
                                )
                except:
                    continue
                if list_products:
                    # print(name_shop, list_products)
                    file = message.file.name
                    file = await client.download_media(message.media, file)
                    print(file)

                    shop = Shop.objects.filter(name=name_shop).first()
                    if not shop:
                        if "$" in list_products[0]["price"]:
                            currency = Currency.objects.get(currency="USD")
                        else:
                            currency = Currency.objects.get(currency="EUR")
                        shop = Shop(name=name_shop, currency=currency)
                        shop.save()
                    post = Post(date=message.date, shop=shop)
                    post.save()

                    if file:
                        img = Image(post=post)
                        with open(str(file), "rb") as file_img:
                            img.image.save(file, File(file_img))
                        img.save()
                    for product in list_products:
                        product["price"] = float(
                            product["price"].replace("$", "").replace("€", "")
                        )
                        item_product = Item(
                            post=post,
                            name=product["name"],
                            link=product["link"],
                            description=product["descr"],
                            cost=product["price"],
                            discount=0,
                        )
                        item_product.save()

            except:
                pass
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open("channel_messages.json", "w", encoding="utf8") as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
    channel = await client.get_entity(-1001769191780)
    await dump_all_messages(channel)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegrambot.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()
    with client:
        client.loop.run_until_complete(main())
