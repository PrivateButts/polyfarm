from django.contrib import admin

from farm.models import Printer, Location


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "handler_type", "handler_id")
    search_fields = ("name", "location__name")
    list_filter = ("location", "handler_type")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)
