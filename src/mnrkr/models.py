from django.db import models
from polyfarm.helpers.models import BaseHandlerModel
from mnrkr.handler import Handler


class MoonrakerConnection(BaseHandlerModel):
    """
    Represents a connection to a Moonraker server.
    """

    url = models.URLField()
    api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.url

    def handler(self):
        return Handler(self.url, self.api_key)

    class Meta(BaseHandlerModel.Meta):
        verbose_name = "Moonraker Connection"
        verbose_name_plural = "Moonraker Connections"


def handler_create(data):
    """Creates a new Moonraker connection handler."""
    return MoonrakerConnection.objects.create(
        url=data.get("url"),
        api_key=data.get("api_key"),
    )


HANDLER_MODEL = MoonrakerConnection
