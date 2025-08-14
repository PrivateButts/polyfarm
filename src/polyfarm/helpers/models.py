from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from polyfarm.helpers import PrinterStatuses


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields for all models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class BaseInfoModel(BaseModel):
    """
    Abstract base model for info models that provides common fields.
    """

    make = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    status = models.IntegerField(
        choices=PrinterStatuses,
        default=0,
    )
    progress = models.FloatField(default=0.0)  # 0-100
    message = models.TextField(blank=True, null=True)
    temperatures = models.JSONField(default=dict)  # Store temperatures as a JSON object

    class Meta(BaseModel.Meta):
        abstract = True


class BaseHandlerModel(BaseModel):
    printer = GenericRelation(
        "farm.Printer",
        content_type_field="handler_type",
        object_id_field="handler_id",
    )

    @property
    def printer_name(self):
        if self.printer.exists():
            return self.printer.first().name
        return "No Printer Assigned"

    class Meta(BaseModel.Meta):
        abstract = True
