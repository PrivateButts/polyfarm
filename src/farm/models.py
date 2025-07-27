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

    # Generic fields for printer handler
    handler_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    handler_id = models.PositiveIntegerField()
    handler_obj = GenericForeignKey("handler_type", "handler_id")

    def __str__(self):
        return self.name

    @property
    def handler(self):
        if not self.handler_obj:
            return None
        return self.handler_obj.handler()

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(fields=["handler_type", "handler_id"]),
        ]


class PrinterHandler(BaseModel):
    class Meta(BaseModel.Meta):
        abstract = True

    name = models.CharField(max_length=100)
