from django_unicorn.components import UnicornView
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from polyfarm.helpers.models import BaseHandlerModel
from farm.models import Printer, Location


class PrinterCreateFormView(UnicornView):
    locations = Location.objects.none()
    handler_form = ""
    handler_type = ""
    printer_name = ""
    printer_loc = Location
    printer_connection = BaseHandlerModel

    def mount(self):
        self.locations = Location.objects.all()
        self.printer_loc = self.locations[0]

    def create_printer(self):
        """Saves the printer data to the database."""

        with transaction.atomic():
            printer = Printer.objects.create(
                name=self.printer_name,
                location=self.printer_loc,
                handler_type=ContentType.objects.get_for_model(self.printer_connection),
                handler_id=self.printer_connection.pk,
            )
            printer.save()
        return printer
