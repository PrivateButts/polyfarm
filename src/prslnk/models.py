from django.db import models
from polyfarm.helpers.models import BaseHandlerModel, BaseInfoModel
from prslnk.handler import Handler


class PrusaLinkPrinterInfoModel(BaseInfoModel):
    """
    Represents the info model for a PrusaLink printer.
    """

    make = models.CharField(max_length=100, default="Prusa Research")
    model = models.CharField(max_length=100)

    class Meta(BaseInfoModel.Meta):
        verbose_name_plural = "Printer Info Objects"
        verbose_name = "Printer Info"


class PrusaLinkConnection(BaseHandlerModel):
    """
    Represents a connection to a PrusaLink server.
    """

    url = models.URLField()
    api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.url

    def handler(self):
        return Handler(self)

    class Meta(BaseHandlerModel.Meta):
        verbose_name = "PrusaLink Connection"
        verbose_name_plural = "PrusaLink Connections"


def handler_create(data):
    """Creates a new PrusaLink connection handler."""
    return PrusaLinkConnection.objects.create(
        url=data.get("url"),
        api_key=data.get("api_key"),
    )


DATA_MODEL = PrusaLinkPrinterInfoModel
HANDLER_MODEL = PrusaLinkConnection
