from polyfarm.helpers.handlers import BaseHandler
import bambulabs_api as bl
import atexit
from asgiref.sync import sync_to_async, async_to_sync


class Handler(BaseHandler):
    def __init__(self, conn):
        super().__init__(conn)
        self.printer = bl.Printer(conn.ip, conn.serial_number, conn.access_token)
        self.printer.mqtt_start()
        atexit.register(self.printer.mqtt_stop)

    @async_to_sync
    async def get_info(self) -> BaseHandler.PrinterInfo:
        printer = await self.connection.printer.afirst()
        info = await sync_to_async(lambda: printer.info)()  # Garbage
        return BaseHandler.PrinterInfo(
            name=printer.name,
            make=info.make,
            model=info.model,
        )

    def _status_map(self, state: bl.GcodeState) -> BaseHandler.statuses:
        if state == bl.GcodeState.IDLE:
            return BaseHandler.statuses.IDLE
        elif state in [bl.GcodeState.PREPARE, bl.GcodeState.RUNNING]:
            return BaseHandler.statuses.PRINTING
        elif state == bl.GcodeState.PAUSE:
            return BaseHandler.statuses.PAUSED
        elif state == bl.GcodeState.FINISH:
            return BaseHandler.statuses.FINISHED
        elif state == bl.GcodeState.FAILED:
            return BaseHandler.statuses.ERROR
        else:
            return BaseHandler.statuses.UNKNOWN

    def get_status(self) -> BaseHandler.PrinterStatus:
        state = self.printer.get_state()
        progress = self.printer.get_percentage()
        if progress is None or progress == "Unknown":
            progress = 0.0
        else:
            progress = float(progress)
        message = ""  # I don't think BambuLab API provides a message directly

        temperatures = {
            "bed": self.printer.get_bed_temperature(),
            "nozzle": self.printer.get_nozzle_temperature(),
        }
        return BaseHandler.PrinterStatus(
            status=self._status_map(state),
            progress=progress,
            message=message,
            temperatures=temperatures,
        )
