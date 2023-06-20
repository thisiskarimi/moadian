

PRIORITIES = ["normal", "fast"]


class Moadian():
    base_url = "https://tp.tax.gov.ir/req/api/{mode}/sync"

    def __init__(self, username, private_key, mode="self-tsp") -> None:
        self.private_key = private_key
        self.username = username
        self.data = {"time": 1, "signature": ""}
        self.base_url = self.base_url.format(mode=mode)
