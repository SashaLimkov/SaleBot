from asgiref.sync import sync_to_async
from typing import List
from bot_backend.models import Shop


@sync_to_async
def get_shops_name() -> List[str]:
    return [item.name for item in Shop.objects.all()]


@sync_to_async
def get_shops() -> List[str]:
    return Shop.objects.all()


@sync_to_async
def get_shop_by_name(name: str) -> Shop:
    return Shop.objects.filter(name=name).first()
