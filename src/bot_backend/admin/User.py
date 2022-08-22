from django.contrib import admin

from ..models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "number"]
    list_display_links = ["name"]
    search_fields = ["name", "email", "number"]


admin.site.register(User, UserAdmin)
