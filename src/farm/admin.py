from django.contrib import admin

from farm.models import Printer, Location, Client, Order, Task, Job


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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "organization")
    search_fields = ("name", "email", "organization")
    ordering = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "created_at", "status")
    search_fields = ("id", "client__name")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "printer", "status", "created_at")
    search_fields = ("id", "order__id", "printer__name")
    list_filter = ("status", "printer")
    ordering = ("-created_at",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "printer", "started_at", "finished_at", "status")
    search_fields = ("id", "task__id", "printer__name")
    list_filter = ("status", "printer")
    ordering = ("-started_at",)
