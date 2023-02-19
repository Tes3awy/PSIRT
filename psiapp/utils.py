"""Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
            https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

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
