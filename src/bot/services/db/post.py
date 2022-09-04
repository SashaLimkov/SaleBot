from asgiref.sync import sync_to_async
from typing import List
from bot_backend.models import Post, Item, Shop, Image


@sync_to_async
def get_post_by_date_shop(date, shop) -> List[Post]:
    shop = Shop.objects.filter(name=shop).first()
    return {
        item: {
            "items": Item.objects.filter(post=item),
            "images": Image.objects.filter(post=item),
        }
        for item in Post.objects.filter(date=date, shop=shop)
    }
