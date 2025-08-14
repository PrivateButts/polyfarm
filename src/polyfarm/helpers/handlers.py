import importlib
from dataclasses import dataclass
from polyfarm.helpers import PrinterStatuses
from polyfarm.helpers.models import BaseHandlerModel


def get_handler(handler, obj):
    """Dynamically imports the appropriate handler form based on the selected handler type.

    Import path should be in the format '{handler}.components.handler_form'.
    """
    print(f"Getting handler form for: {handler}")
    if not handler:
        return None

    try:
        target = obj.split(".")
        module_path = f"{handler}.{'.'.join(target[:-1])}"
        handler_module = importlib.import_module(module_path)
        return getattr(handler_module, target[-1])
    except (ModuleNotFoundError, AttributeError, ValueError) as e:
        raise e


class BaseHandler:
    class HandlerError(Exception):
        pass

    def __init__(self, connection: BaseHandlerModel):
        """Base handler class for printer handlers."""
        self.connection = connection

    @dataclass
    class PrinterInfo:
        name: str
        make: str
        model: str

    def get_info(self) -> PrinterInfo:
        """Fetches the current status of the printer"""
        raise NotImplementedError("Base Handler Method Called")

    @dataclass
    class PrinterStatus:
        status: PrinterStatuses
        progress: float  # 0-100
        message: str
        temperatures: dict

    def get_status(self) -> PrinterStatus:
        """Returns the current status of the printer"""
        raise NotImplementedError("Base Handler Method Called")

    def poll_printer(self):
        """Polls the printer for its current status and updates the database."""
        status = self.get_status()
        info = self.get_info()
        info_storage = self.connection.printer.info
        info_storage.name = info.name
        info_storage.make = info.make
        info_storage.model = info.model

        info_storage.status = status.status
        info_storage.progress = status.progress
        info_storage.message = status.message
        info_storage.temperatures = status.temperatures

        info_storage.save()
