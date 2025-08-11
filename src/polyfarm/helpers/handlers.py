import importlib
from enum import Enum
from dataclasses import dataclass


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

    class statuses(Enum):
        UNKNOWN = 0
        IDLE = 1
        READY = 2
        PRINTING = 3
        PAUSED = 4
        ERROR = 5
        FINISHED = 6

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
        status: "BaseHandler.statuses"
        progress: float
        message: str
        temperatures: dict

    def get_status(self) -> PrinterStatus:
        """Returns the current status of the printer"""
        raise NotImplementedError("Base Handler Method Called")
