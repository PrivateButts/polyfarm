from pyprusalink import PrusaLink
from httpx import AsyncClient
from asgiref.sync import async_to_sync, sync_to_async

from polyfarm.helpers.handlers import BaseHandler


class Handler(BaseHandler):
    def __init__(self, conn):
        super().__init__()
        self.api_url = conn.url
        self.api_key = conn.api_key
        self.conn = conn
        self.client = AsyncClient()
        self.pl = PrusaLink(
            async_client=self.client, host=self.api_url, username="maker", password=self.api_key
        )

    @async_to_sync
    async def get_info(self) -> BaseHandler.PrinterInfo:
        printer = await self.conn.printer.afirst()
        info = await sync_to_async(lambda: printer.info)()  # Garbage
        return BaseHandler.PrinterInfo(
            name=printer.name,
            make=info.make,
            model=info.model,
        )

    def _status_map(self, status):
        status_map = {
            "IDLE": BaseHandler.statuses.IDLE,
            "READY": BaseHandler.statuses.READY,
            "PRINTING": BaseHandler.statuses.PRINTING,
            "PAUSED": BaseHandler.statuses.PAUSED,
            "ERROR": BaseHandler.statuses.ERROR,
            "FINISHED": BaseHandler.statuses.FINISHED,
        }
        return status_map.get(status, BaseHandler.statuses.UNKNOWN)

    @async_to_sync
    async def get_status(self) -> BaseHandler.PrinterStatus:
        status_response = (await self.pl.get_status()).get("printer")
        status = BaseHandler.statuses(self._status_map(status_response.get("state", "UNKNOWN")))
        progress = 0.0
        if status == BaseHandler.statuses.PRINTING:
            job = await self.pl.get_job()
            progress = job.get("progress", 0.0)
        return BaseHandler.PrinterStatus(
            status=status,
            progress=progress,
            message=status_response.get("message", ""),
            temperatures={
                "bed": status_response.get("temp_bed", 0),
                "nozzle": status_response.get("temp_nozzle", 0),
            },
        )
