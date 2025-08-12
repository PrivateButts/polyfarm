from benedict import benedict
from polyfarm.helpers.handlers import BaseHandler
import httpx


class Handler(BaseHandler):
    def __init__(self, api_url, api_key=None):
        super().__init__()
        url = api_url if api_url.endswith("/") else f"{api_url}/"
        self.client = httpx.Client(base_url=url, headers={"X-Api-Key": api_key} if api_key else {})

    def _request(self, method, endpoint, **kwargs) -> benedict:
        response = self.client.request(method, endpoint, **kwargs)
        response.raise_for_status()
        return benedict(response.json())

    def get_info(self) -> BaseHandler.PrinterInfo:
        info = self._request("get", "/printer/info").result
        name = info.hostname
        make = "Unknown"  # Placeholder, actual value should be fetched from info
        model = "Unknown"  # Placeholder, actual value should be fetched from info
        return BaseHandler.PrinterInfo(
            name=name,
            make=make,
            model=model,
        )

    def _status_map(self, state):
        status_map = {
            "standby": BaseHandler.statuses.IDLE,
            "printing": BaseHandler.statuses.PRINTING,
            "paused": BaseHandler.statuses.PAUSED,
            "cancelled": BaseHandler.statuses.ERROR,
            "error": BaseHandler.statuses.ERROR,
            "complete": BaseHandler.statuses.FINISHED,
        }
        return status_map.get(state.lower(), BaseHandler.statuses.UNKNOWN)

    def get_status(self) -> BaseHandler.PrinterStatus:
        status = self._request(
            "get",
            "/printer/objects/query?print_stats=state,message,filename&heater_bed=temperature&extruder=temperature&virtual_sdcard=progress,is_active&display_status=message",
        ).result.status
        state = status.get_str("print_stats.state", "unknown")
        progress = status.get_float("virtual_sdcard.progress", 0.0) * 100.0
        stats_message = status.get_str("print_stats.message", "")
        display_message = status.get_str("display_status.message", "")
        message = stats_message if stats_message else display_message

        temperatures = {
            "bed": status.get_float("heater_bed.temperature", 0),
            "nozzle": status.get_float("extruder.temperature", 0),
        }
        return BaseHandler.PrinterStatus(
            status=self._status_map(state),
            progress=progress,
            message=message,
            temperatures=temperatures,
        )
