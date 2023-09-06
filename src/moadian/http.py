import json
import time
import uuid
import requests


def init_headers():
    headers = {'timestamp': str(int(time.time() * 1000)),
               'requestTraceId': str(uuid.uuid4())}
    return headers


def send_req(url, headers, data):
    headers["Content-Type"] = 'application/json'
    res = requests.post(url, data=json.dumps(data), headers=headers)
    return res
