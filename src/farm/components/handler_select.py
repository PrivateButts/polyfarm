from django_unicorn.components import UnicornView
from django.db import models

from polyfarm.helpers.handlers import get_handler


class HandlerSelectView(UnicornView):
    selection = None
    connections = models.QuerySet()
    handler_name = ""

    def mount(self):
        model = get_handler(self.handler_name, "models.HANDLER_MODEL")
        self.connections = model.objects.all()
        if self.connections.exists():
            print(self.connections.first())
            self.parent.printer_connection = self.connections.first()

    def updated_selection(self, value):
        self.parent.printer_connection = value
