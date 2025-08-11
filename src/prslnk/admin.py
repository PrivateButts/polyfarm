from django.contrib import admin

from .models import PrusaLinkConnection, PrusaLinkPrinterInfoModel


@admin.register(PrusaLinkConnection)
class PrusaLinkConnectionAdmin(admin.ModelAdmin):
    list_display = ("url", "printer_name", "created_at", "updated_at")
    search_fields = ("url", "api_key")


@admin.register(PrusaLinkPrinterInfoModel)
class PrusaLinkPrinterInfoModelAdmin(admin.ModelAdmin):
    list_display = ("make", "model", "created_at", "updated_at")
    search_fields = ("make", "model")
    list_filter = ("make", "model")
    ordering = ("-created_at",)
