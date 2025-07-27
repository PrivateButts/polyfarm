import importlib
from enum import Enum


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
    class statuses(Enum):
        OFFLINE = 0
        ONLINE = 1

    def get_info(self):
        """Fetches the current status of the printer"""
        raise NotImplementedError("Base Handler Method Called")
