from asgiref.sync import sync_to_async
from .currency import get_currency_by_name
from bot_backend.models import SettingsUserShop, FormulaPrice, User, Shop


@sync_to_async
def get_settings_shop_user_by_user(user_id: int, shop: str) -> SettingsUserShop:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    return SettingsUserShop.objects.filter(user=user, shop=shop).first()


@sync_to_async
def update_currency_settings_shop_user(user_id: int, shop: str, currency: str) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop)
    user_settings.currency = get_currency_by_name(currency)
    user_settings.save()


@sync_to_async
def update_formula_settings_shop_user(user_id: int, shop: str, formula: int) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop)
    user_settings.formula = FormulaPrice.objects.all()[formula]
    user_settings.save()


@sync_to_async
def update_post_settings_shop_user(user_id: int, shop: str, post: int) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop)
    user_settings.post = post
    user_settings.save()


@sync_to_async
def update_signature_settings_shop_user(
    user_id: int, shop: str, signature: str
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop)
    user_settings.signature = signature
    user_settings.save()


@sync_to_async
def update_language_settings_shop_user(user_id: int, shop: str, language: str) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop)
    user_settings.signature = language
    user_settings.save()


@sync_to_async
def update_link_settings_shop_user(user_id: int, shop: str, link: bool) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop)
    user_settings.signature = link
    user_settings.save()


@sync_to_async
def update_product_link_settings_shop_user(
    user_id: int, shop: str, value: bool
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop).first()
    user_settings.product.link = value
    user_settings.save()


@sync_to_async
def update_product_name_settings_shop_user(
    user_id: int, shop: str, value: bool
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop).first()
    user_settings.product.name = value
    user_settings.save()


@sync_to_async
def update_product_price_settings_shop_user(
    user_id: int, shop: str, value: bool
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop).first()
    user_settings.product.price = value
    user_settings.save()


@sync_to_async
def update_product_discount_settings_shop_user(
    user_id: int, shop: str, value: bool
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop).first()
    user_settings.product.discount = value
    user_settings.save()


@sync_to_async
def update_product_weight_settings_shop_user(
    user_id: int, shop: str, value: bool
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop).first()
    user_settings.product.weight = value
    user_settings.save()


@sync_to_async
def update_product_description_settings_shop_user(
    user_id: int, shop: str, value: bool
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop).first()
    user_settings.product.description = value
    user_settings.save()


@sync_to_async
def update_product_size_settings_shop_user(
    user_id: int, shop: str, value: bool
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop).first()
    user_settings.product.size = value
    user_settings.save()


@sync_to_async
def update_product_compound_settings_shop_user(
    user_id: int, shop: str, value: bool
) -> None:
    user = User.objects.filter(user_id=user_id).first()
    shop = Shop.objects.filter(name=shop).first()
    user_settings = SettingsUserShop.objects.filter(user=user, shop=shop).first()
    user_settings.product.compound = value
    user_settings.save()
