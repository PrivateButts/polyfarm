from django.db import models
from polyfarm.helpers.models import BaseHandlerModel, BaseInfoModel
from bblb.handler import Handler


class BambuPrinterInfoModel(BaseInfoModel):
    """
    Represents the info model for a Bambu printer.
    """

    make = models.CharField(max_length=100, default="Bambu Labs")


class BambuConnection(BaseHandlerModel):
    """
    Represents a connection to a Bambu server.
    """

    ip = models.GenericIPAddressField()
    serial_number = models.CharField(max_length=100)
    access_code = models.CharField(max_length=100)

    def __str__(self):
        return self.serial_number

    def handler(self):
        return Handler(self)

    class Meta(BaseHandlerModel.Meta):
        verbose_name = "Bambu Labs Connection"
        verbose_name_plural = "Bambu Labs Connections"


def handler_create(data):
    """Creates a new Bambu connection handler."""
    return BambuConnection.objects.create(
        ip=data.get("ip"),
        serial_number=data.get("serial_number"),
        access_code=data.get("access_code"),
    )


HANDLER_MODEL = BambuConnection
