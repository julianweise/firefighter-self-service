from django.contrib import admin
from django.contrib.admin import ModelAdmin

from equipment.models import Pager, Locker, Key, Room


class CustomPagerAdmin(ModelAdmin):
    list_display = ("pager_id",)
    list_filter = ("pager_id",)
    search_fields = ("pager_id",)
    ordering = ("pager_id",)


admin.site.register(Pager, CustomPagerAdmin)


class CustomLockerAdmin(ModelAdmin):
    list_display = ("locker_id",)
    list_filter = ("locker_id",)
    search_fields = ("locker_id",)
    ordering = ("locker_id",)


admin.site.register(Locker, CustomLockerAdmin)


class CustomRoomAdmin(ModelAdmin):
    list_display = ("room_id", "name")
    list_filter = ("room_id", "name")
    search_fields = ("room_id", "name")
    ordering = ("room_id", "name")


admin.site.register(Room, CustomRoomAdmin)
admin.site.register(Key)
