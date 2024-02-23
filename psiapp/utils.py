import math

import requests
from flask import current_app


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r: requests.Request):
        r.headers["Authorization"] = f"Bearer {self.token}"
        r.headers["Content-Type"] = "application/json"
        r.headers["Accept"] = "application/json"
        return r


def fetch_data(uri: str, access_token: str) -> requests.Response:
    url = f"{current_app.config.get('BASE_URL')}/{uri}"
    r = requests.get(url=url, auth=BearerAuth(access_token), verify=False)
    r.raise_for_status()
    return r


def paginate(paging: dict, pageIndex: int = 1, pageSize: int = 10) -> dict[str, int]:
    total_count: int = paging.get("count")
    tnp = math.ceil(total_count / pageSize)  # total number of pages
    start = (pageIndex - 1) * pageSize
    end = min(start + pageSize, total_count)
    return {"tnp": tnp, "total_count": total_count, "start": start, "end": end}
