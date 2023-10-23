import os
import json
import tempfile
from .packet import Packet
from .http import init_headers, send_req
from .normalizer import normalize_json
from .encryption import sign, xor_and_encrypt_data, encrypt_aes_key


PRIORITIES = ["normal", "fast"]


class Moadian():
    base_url = "https://tp.tax.gov.ir/req/api/{mode}/sync"

    def __init__(self, fiscal_id, private_key, mode="self-tsp") -> None:
        self.private_key = private_key
        self.fiscal_id = fiscal_id
        self.base_url = self.base_url.format(mode=mode)

    def _get_tax_gov_key(self):
        # look for a file containing key
        temp_dir = tempfile.gettempdir()
        filename = "tax_gov_key"
        where_to_find = os.path.join(temp_dir, filename)
        if os.path.isfile(where_to_find):
            try:
                with open(where_to_find) as f:
                    k = json.load(f.read())
                return k['id'], k['key']
            except Exception:
                pass
        srv_info = self.get_server_information()
        k = srv_info["result"]["data"]["publicKeys"][0]
        # save it for further uses
        with open(where_to_find, 'w') as f:
            json.dump(srv_info["result"]["data"]["publicKeys"][0], f)
        return k['id'], k['key']

    def _parse_invoice(self, invoice):
        if isinstance(invoice, dict):
            return invoice
        if isinstance(invoice, str):
            return json.loads(invoice)
        raise Exception("Invalid invoice!")

    def get_server_information(self):
        url = self.base_url + "/GET_SERVER_INFORMATION"
        headers = init_headers()
        data = {"time": 1, "signature": ""}
        data["packet"] = Packet("GET_SERVER_INFORMATION",
                                self.fiscal_id).to_dict()
        r = send_req(url, headers, data)
        return json.loads(r.text)

    def get_economic_code_information(self, economic_code):
        data = {"time": 1, "packet": None, "signature": ""}
        url = self.base_url + "/GET_ECONOMIC_CODE_INFORMATION"
        headers = init_headers()
        data["packet"] = Packet("GET_ECONOMIC_CODE_INFORMATION", self.fiscal_id, {
            "economicCode": economic_code},).to_dict()
        r = send_req(url, headers, data)
        return json.loads(r.text)

    def get_token(self):
        url = self.base_url + "/GET_TOKEN"
        data = {"time": 1, "packet": None, "signature": ""}
        data["packet"] = Packet("GET_TOKEN", self.fiscal_id, {
                                'username': self.fiscal_id}).to_dict()
        headers = init_headers()
        res = normalize_json(data["packet"], headers)
        data["signature"] = sign(res, self.private_key)
        res = send_req(url, headers, data)
        return json.loads(res.text)

    def send_invoice(self, invoice, priority="normal"):
        invoice = self._parse_invoice(invoice)
        if priority not in PRIORITIES:
            raise Exception("Invalid priority!")
        url = self.base_url[:-5] + "/async/"+priority+"-enqueue"
        data = {"time": 1, "packets": None, "signature": ""}
        data['packets'] = [Packet('INVOICE.V01', self.fiscal_id).to_dict()]
        data['packets'][0]['data'] = invoice
        normalized = normalize_json(invoice)
        data['packets'][0]['dataSignature'] = sign(
            normalized, self.private_key)
        key = os.urandom(32).hex()
        iv = os.urandom(16).hex()
        tax_gov_key_id, tax_gov_public_key = self._get_tax_gov_key()
        data['packets'][0]['iv'] = iv
        data['packets'][0]['symmetricKey'] = encrypt_aes_key(
            tax_gov_public_key, key)
        data['packets'][0]['encryptionKeyId'] = tax_gov_key_id
        data['packets'][0]['data'] = xor_and_encrypt_data(
            data['packets'][0]['data'],
            key,
            iv
        )
        headers = init_headers()
        token = self.get_token()['result']['data']['token']
        clonhead = headers.copy()
        clonhead["Authorization"] = token
        headers["Authorization"] = "Bearer " + token
        res = normalize_json({"packets": data['packets']}, clonhead)
        data['signature'] = sign(res, self.private_key)
        re = send_req(url, headers, data)
        return json.loads(re.text)

    def inquiry_by_reference_number(self, reference_number):
        url = self.base_url + "/INQUIRY_BY_REFERENCE_NUMBER"
        data = {"time": 1, "packet": None, "signature": ""}
        data["packet"] = Packet('INQUIRY_BY_REFERENCE_NUMBER', self.fiscal_id, {
                                "referenceNumber": [reference_number]}).to_dict()
        headers = init_headers()
        token = self.get_token()['result']['data']['token']
        copied_headers = headers.copy()
        copied_headers["Authorization"] = token
        headers["Authorization"] = "Bearer " + token
        res = normalize_json(data["packet"], copied_headers)
        data["signature"] = sign(res, self.private_key)
        res = send_req(url, headers, data)
        return json.loads(res.text)
