from django.contrib import admin

from ..models import (
    SettingsUser,
    FormulaPrice,
    Currency,
    ProductSettings,
    Shop,
    Image,
    Post,
    Item,
)


class ItemInline(admin.TabularInline):
    model = Item


class ImageInline(admin.TabularInline):
    model = Image


class PostAdmin(admin.ModelAdmin):
    inlines = [ItemInline, ImageInline]


admin.site.register(SettingsUser)
admin.site.register(FormulaPrice)
admin.site.register(Currency)
admin.site.register(ProductSettings)
admin.site.register(Shop)
admin.site.register(Image)
admin.site.register(Post, PostAdmin)
admin.site.register(Item)
