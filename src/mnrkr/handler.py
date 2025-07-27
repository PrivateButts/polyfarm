from polyfarm.helpers.handlers import BaseHandler
import requests


class Handler(BaseHandler):
    def __init__(self, api_url, api_key=None):
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key
        self._headers = {"X-Api-Key": api_key} if api_key else {}

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.api_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        all_headers = {**self._headers, **headers}
        try:
            response = requests.request(method, url, headers=all_headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_info(self):
        return self._request("get", "/printer/info")

    def query_objects(self, objects=None):
        params = {"objects": objects} if objects else {}
        return self._request("get", "/printer/objects/query", params=params)

    def start_print(self, filename):
        return self._request("post", "/server/files/print", json={"filename": filename})

    def cancel_print(self):
        return self._request("post", "/printer/print/cancel")
