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

    user_id = models.BigIntegerField(unique=True, verbose_name="UserID")
    nickname = models.CharField(max_length=255, verbose_name="nickname")
    name = models.CharField(max_length=255, verbose_name="Имя", )
    second_name = models.CharField(max_length=255, verbose_name="Фамилия", )
    number = models.CharField(max_length=255, verbose_name="Номер телефона")
    email = models.CharField(max_length=355, verbose_name="Почта")
    city = models.CharField(max_length=255, verbose_name="Город")
