from django.db.models import IntegerChoices


class PrinterStatus(IntegerChoices):
    UNKNOWN = 0, "Unknown"
    IDLE = 1, "Idle"
    READY = 2, "Ready"
    PRINTING = 3, "Printing"
    PAUSED = 4, "Paused"
    ERROR = 5, "Error"
    FINISHED = 6, "Finished"
