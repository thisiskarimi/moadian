import json
from .packet import Packet
from .http import init_headers, send_req


PRIORITIES = ["normal", "fast"]


class Moadian():
    base_url = "https://tp.tax.gov.ir/req/api/{mode}/sync"

    def __init__(self, fiscal_id, private_key, mode="self-tsp") -> None:
        self.private_key = private_key
        self.fiscal_id = fiscal_id
        self.data = {"time": 1, "signature": ""}
        self.base_url = self.base_url.format(mode=mode)

    def get_server_information(self):
        url = self.base_url + "/GET_SERVER_INFORMATION"
        headers = init_headers()
        data = {"time": 1, "signature": ""}
        data["packet"] = Packet("GET_SERVER_INFORMATION",
                                self.fiscal_id).to_dict()
        r = send_req(url, headers, data)
        return json.loads(r.text)

    def get_economic_code_information(self, economic_code):
        url = self.base_url + "/GET_ECONOMIC_CODE_INFORMATION"
        headers = init_headers()
        self.data["packet"] = Packet("GET_ECONOMIC_CODE_INFORMATION", self.fiscal_id, {
            "economicCode": economic_code},).to_dict()
        r = send_req(url, headers, self.data)
        return json.loads(r.text)
