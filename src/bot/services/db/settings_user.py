from asgiref.sync import sync_to_async
from django.core.files import File

from .currency import get_currency_by_name
from bot_backend.models import (
    SettingsUser,
    FormulaPrice,
    User,
    Currency,
    ProductSettings,
)
from random import randint


@sync_to_async
def create_settings_user(user_id: int) -> SettingsUser:
    user = User.objects.filter(user_id=user_id).first()
    settings_product = ProductSettings()
    settings_product.save()
    settings = SettingsUser(
        user=user,
        product=settings_product,
        currency=Currency.objects.all()[0],
        formula=FormulaPrice.objects.all()[0],
    )

    settings.save()


@sync_to_async
def get_settings_user_by_user(user_id: int) -> SettingsUser:
    user = User.objects.filter(user_id=user_id).first()
    return SettingsUser.objects.filter(user=user).first()


@sync_to_async
def get_signature_settings_user(user_id: int) -> bool:
    user = User.objects.filter(user_id=user_id).first()
    return SettingsUser.objects.filter(user=user).first().signature


@sync_to_async
def get_formula_settings_user(user_id: int) -> bool:
    user = User.objects.filter(user_id=user_id).first()
    return SettingsUser.objects.filter(user=user).first().formula.name


@sync_to_async
def get_logo_settings_user(user_id: int) -> bool:
    user = User.objects.filter(user_id=user_id).first()
    return SettingsUser.objects.filter(user=user).first().logo.path


@sync_to_async
def delete_logo_settings_user(user_id: int) -> bool:
    user = User.objects.filter(user_id=user_id).first()
    SettingsUser.objects.filter(user=user).first().logo = None


@sync_to_async
def get_logo_position_settings_user(user_id: int) -> bool:
    user = User.objects.filter(user_id=user_id).first()
    return SettingsUser.objects.filter(user=user).first().logo_position


@sync_to_async
def get_commission_settings_user(user_id: int) -> bool:
    user = User.objects.filter(user_id=user_id).first()
    return SettingsUser.objects.filter(user=user).first().commission


@sync_to_async
def get_formula_by_id_settings_user(formula: int) -> bool:
    return FormulaPrice.objects.all()[int(formula)]


@sync_to_async
def get_currency_settings_user(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return SettingsUser.objects.filter(user=user).first().currency.name


@sync_to_async
def update_currency_settings_user(user_id: int, currency: str) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.currency = Currency.objects.filter(name=currency).first()
    user_settings.save()


@sync_to_async
def update_commission_settings_user(user_id: int, commission: float) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.commission = commission
    user_settings.save()


@sync_to_async
def update_formula_settings_user(user_id: int, formula: int) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.formula = FormulaPrice.objects.all()[formula]
    user_settings.save()


@sync_to_async
def update_logo_settings_user(user_id: int, logo: str) -> None:
    print(2222)
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    with open(logo, "rb") as file:
        user_settings.logo.save(
            str(randint(10000, 9999999)) + "." + logo.split(".")[-1], File(file)
        )
        user_settings.save()


@sync_to_async
def update_logo_position_settings_user(user_id: int, position: str) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.logo_position = position
    user_settings.save()


@sync_to_async
def update_signature_settings_user(user_id: int, signature: str) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.signature = signature
    user_settings.save()


@sync_to_async
def update_language_settings_user(user_id: int, language: str) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.language = language
    user_settings.save()


@sync_to_async
def update_link_settings_user(user_id: int, link: bool) -> None:
    print(user_id, link)
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.link = link
    user_settings.save()


@sync_to_async
def update_product_link_settings_user(user_id: int, value: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.product.link = value
    user_settings.product.save()
    user_settings.save()


@sync_to_async
def update_product_name_settings_user(user_id: int, value: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.product.name = value
    user_settings.product.save()
    user_settings.save()


@sync_to_async
def update_product_price_settings_user(user_id: int, value: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.product.price = value
    user_settings.product.save()
    user_settings.save()


@sync_to_async
def update_product_discount_settings_user(user_id: int, value: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.product.discount = value
    user_settings.product.save()
    user_settings.save()


@sync_to_async
def update_product_weight_settings_user(user_id: int, value: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.product.weight = value
    user_settings.product.save()
    user_settings.save()


@sync_to_async
def update_product_description_settings_user(user_id: int, value: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.product.description = value
    user_settings.product.save()
    user_settings.save()


@sync_to_async
def update_product_size_settings_user(user_id: int, value: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.product.size = value
    user_settings.product.save()
    user_settings.save()


@sync_to_async
def update_product_compound_settings_user(user_id: int, value: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    user_settings = SettingsUser.objects.filter(user=user).first()
    user_settings.product.compound = value
    user_settings.product.save()
    user_settings.save()
