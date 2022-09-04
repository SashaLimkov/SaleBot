from django.db import models


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModel):
    class Meta:
        verbose_name = "Зарегестрированный пользоваетель"
        verbose_name_plural = "Зарегестрированные пользоваетели"

    active = models.BooleanField(verbose_name="Активен")
    user_id = models.BigIntegerField(unique=True, verbose_name="UserID")
    nickname = models.CharField(max_length=255, verbose_name="nickname")
    name = models.CharField(
        max_length=7000,
        verbose_name="ФИО",
    )
    number = models.CharField(max_length=255, verbose_name="Номер телефона")
    count_members = models.IntegerField(verbose_name="Количество помощников")

    def __str__(self):
        return f"{self.user_id} | {self.nickname} | {self.name}"


class Member(models.Model):
    invite_user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пригласивший пользователь"
    )
    active = models.BooleanField(verbose_name="Активен")
    user_id = models.BigIntegerField(verbose_name="Telegram ID")

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = "Помощника"
        verbose_name_plural = "Помощники"


class Chanel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    chat_id = models.BigIntegerField(verbose_name="ID Канала")
    name_channel = models.CharField(max_length=200, verbose_name="Название канала")

    def __str__(self):
        return f"{self.user.nickname} | {self.chat_id}"

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"


class Currency(models.Model):
    name = models.CharField(max_length=5, verbose_name="Название валюты (в боте)")
    currency = models.CharField(max_length=3, verbose_name="Валюта")
    sign = models.CharField(max_length=1, verbose_name="Знак валюты")

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = "Валюту"
        verbose_name_plural = "Валюты"


class Shop(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название магазина")
    currency = models.ForeignKey(
        Currency, verbose_name="Валюта магазина", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class Post(TimeBasedModel):
    date = models.DateField(
        auto_now_add=False, verbose_name="Date", null=True, blank=True
    )
    shop = models.ForeignKey(Shop, verbose_name="Магазин", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Image(models.Model):
    image = models.ImageField(verbose_name="Изображение", blank=True, null=True)
    post = models.ForeignKey(
        Post,
        verbose_name="Пост",
        related_name="image",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Изображение поста"
        verbose_name_plural = "Изображения постов"


class Item(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name="Пост", related_name="items"
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    link = models.CharField(max_length=20000, verbose_name="Ссылка")
    description = models.CharField(
        max_length=20000, verbose_name="Описание", blank=True, null=True
    )
    cost = models.FloatField(verbose_name="Цена")
    discount = models.FloatField(verbose_name="Скидка")

    def __str__(self):
        return f"{self.post.date} | {self.name}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class FormulaPrice(models.Model):
    name = models.CharField(max_length=150, verbose_name="Текст формулы")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Формулу"
        verbose_name_plural = "Формула"


class ProductSettings(models.Model):
    link = models.BooleanField(verbose_name="Ссылка", default=True)
    name = models.BooleanField(verbose_name="Название", default=True)
    price = models.BooleanField(verbose_name="Цена", default=True)
    discount = models.BooleanField(verbose_name="Скидка", default=True)
    description = models.BooleanField(verbose_name="Описание", default=True)

    # size = models.BooleanField(verbose_name="Размер")
    # compound = models.BooleanField(verbose_name="Состав")
    # discount = models.BooleanField(verbose_name="Скидка")
    # weight = models.BooleanField(verbose_name="Вес")
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Настройку товара"
        verbose_name_plural = "Настройки товара"


class SettingsUser(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, verbose_name="Валюта", on_delete=models.CASCADE
    )
    formula = models.ForeignKey(
        FormulaPrice, verbose_name="Формула ценообразования", on_delete=models.CASCADE
    )
    commission = models.FloatField(
        verbose_name="Комиссия", blank=True, null=True, default=0.0
    )
    logo = models.ImageField(verbose_name="Логотип", blank=True, null=True)
    logo_position = models.CharField(
        max_length=10, verbose_name="Позиция лого", blank=True, null=True
    )
    product = models.ForeignKey(
        ProductSettings, verbose_name="Настройки продукта", on_delete=models.CASCADE
    )
    signature = models.TextField(verbose_name="Подпись", default="")
    link = models.BooleanField(verbose_name="Коротка ссылка", default=False)

    def __str__(self):
        return f"{self.user.nickname}"

    class Meta:
        verbose_name = "Общую настройку"
        verbose_name_plural = "Общие настройки пользователей"


class UnloadingTelegram(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название канала")
    id_channel = models.BigIntegerField(verbose_name="ID Канала")
    settings = models.ForeignKey(
        SettingsUser, verbose_name="Настройки", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.settings.user.nickname} | {self.name}"

    class Meta:
        verbose_name = "Настройку товара"
        verbose_name_plural = "Настройки товара"


class SettingsUserShop(models.Model):
    shop = models.ForeignKey(Shop, verbose_name="Магазин", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, verbose_name="Валюта", on_delete=models.CASCADE, default=0
    )
    formula = models.ForeignKey(
        FormulaPrice,
        verbose_name="Формула ценообразования",
        on_delete=models.CASCADE,
        default=0,
    )
    commission = models.FloatField(
        verbose_name="Комиссия", blank=True, null=True, default=0.0
    )
    logo = models.ImageField(verbose_name="Логотип", blank=True, null=True)
    product = models.ForeignKey(
        ProductSettings, verbose_name="Настройки продукта", on_delete=models.CASCADE
    )
    signature = models.TextField(verbose_name="Подпись", default="")
    link = models.BooleanField(verbose_name="Коротка ссылка", default=False)

    def __str__(self):
        return f"{self.user.nickname} | {self.shop.name}"

    class Meta:
        verbose_name = "Настройку магазига"
        verbose_name_plural = "Настройки магазинов пользователей"
