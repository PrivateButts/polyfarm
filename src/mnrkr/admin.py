from django.contrib import admin

from mnrkr.models import MoonrakerConnection


@admin.register(MoonrakerConnection)
class MoonrakerConnectionAdmin(admin.ModelAdmin):
    list_display = ("url",)
    search_fields = ("url",)
    ordering = ("url",)
