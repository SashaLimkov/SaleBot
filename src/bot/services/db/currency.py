from asgiref.sync import sync_to_async
from typing import List
from bot_backend.models import Currency


@sync_to_async
def get_currency() -> List[str]:
    return [item.name for item in Currency.objects.all()]


@sync_to_async
def get_currency_by_name(name: str) -> Currency:
    return Currency.objects.filter(name=name).first()
