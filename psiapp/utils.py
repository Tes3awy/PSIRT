import math

import requests
from flask import current_app as app


def fetch_data(uri: str, access_token: str) -> requests.Response:
    r = requests.get(
        url=f"{app.config['BASE_URL']}/{uri}",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Set-Cookie": "SameSite=None;",
            "Authorization": f"Bearer {access_token}",
        },
        verify=False,
    )
    r.raise_for_status()
    return r


def get_pagination(paging: dict, pageIndex: int) -> dict[str, int]:
    total_count: int = paging.get("count")
    tnp = math.ceil(total_count / 10)  # total number of pages
    start = (pageIndex - 1) * 10
    end = min(start + 10, total_count)
    return {"tnp": tnp, "total_count": total_count, "start": start, "end": end}
