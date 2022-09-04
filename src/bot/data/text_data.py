CLIENT_REG_MENU = (
    "{nickname}, здравствуйте!\n"
    "Пожалуйста, заполните следующие данные о себе:\n"
    "<b>ФИО</b>: {name}\n"
    "<b>Номер телефона</b>: {number}\n"
)

GET_NAME = "Укажите ФИО"
GET_NUMBER = "Укажите Ваш контактный номер телефона"
MM_TEXT = """1. Для настройки анонсов зайдите в пункт меню НАСТРОЙКИ
2. В пункте ПОДПИСКИ собраны подписки
3. В пункте ШАБЛОНЫ есть возможность сформировать индивидуальные настройки под каждый магазин
4. В пункте АНОНСЫ представлены анонсы, которые после настройки можно отправить клиентам"""
MM_ANONS = "Анонсы"
MM_PSBT = """Выберите параметр для настройки.
Здесь можно:
- выбрать базовую валюту для анонса;
- определить формулу для формирования цены и выбрать комиссию;
- настроить изображение(пост) и информацию о товаре в анонсе;
- создать свою уникальную подпись;
- настроить язык анонса;
- выбрать формат ссылки;
- настроить канал и контакты для выгрузки анонса."""
MM_S_CUR = """Здесь можно:
Выбрать валюту для всех анонсов

Ваши настройки валюты и курса:

Выбранная валюта - <b>{cur}</b>"""
MM_FORMULA = """Здесь можно выбрать формулу, для формирования цены товара (1 из 3)
Кнопка ВПЕРЕД (⏩)- переход к следующей формуле
Кнопка НАЗАД (⏪) - переход к предыдущей формуле
Назначенная вами комиссия - {com}
Выбранная формула: <b>{selected}</b>

пример:
{formula}

A - цена (100$)
B - скидка на сайте (30%) - скидка берется из анонса автоматически
C - комиссия (10%)"""
MM_POST = """Здесь можно загрузить собственное лого:

Ваши текущие настройки изображений в анонсе:
"""
MM_INFO = """Меню настроек информации о товаре в анонсе.

Ваши текущие настройки "О товаре":
"""
MM_SIGN = "Ваша подпись: {sign}."
MM_LANG = """В этом меню вы можете выбрать язык для всех анонсов.

Ваши текущее настройки:
Язык анонса - Язык сайта"""
MM_SH_LINK = """В этом меню вы можете выбрать вид ссылок для всех анонсов.
"""
MM_GET = "Выберите мессенджер для выгрузки"

COMPLETE_DESCR = "Подпись успешно добавлена"
MM_ADD_PHOTO = """Сначала загрузите фото
"""
MM_ADD_HELPER = "Количество помощников {count}\n{link}"
