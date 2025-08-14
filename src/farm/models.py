from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from polyfarm.helpers.models import BaseModel


class Location(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Printer(BaseModel):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="printers")

    # Generic fields for printer info
    info_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, related_name="printer_info", null=True, blank=True
    )
    info_id = models.PositiveIntegerField(blank=True, null=True)
    info_obj = GenericForeignKey("info_type", "info_id")

    # Generic fields for printer handler
    handler_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        related_name="printer_handler",
        null=True,
        blank=True,
    )
    handler_id = models.PositiveIntegerField(blank=True, null=True)
    handler_obj = GenericForeignKey("handler_type", "handler_id")

    def __str__(self):
        return self.name

    @property
    def handler(self):
        if not self.handler_obj:
            return None
        return self.handler_obj.handler()

    @property
    def info(self):
        if not self.info_obj:
            return None
        return self.info_obj


class Client(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)


class Order(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")


class Task(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tasks")
    model = models.FileField(upload_to="orders/models/")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order {self.order.id} - Task {self.id} ({self.quantity})"


class Job(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="jobs")
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name="jobs")
    plate = models.FileField(upload_to="jobs/plates/", blank=True, null=True)

    def __str__(self):
        return f"Job {self.id} for Task {self.task.id} on Printer {self.printer.name}"
