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

import requests
from flask import flash, redirect, url_for


def fetch_products(prodType: str = "CISCO") -> list[dict]:
    try:
        r = requests.get(
            # https://tools.cisco.com/security/center/productBoxData.x
            url="https://sec.cloudapps.cisco.com/security/center/productBoxData.x",
            params={"prodType": prodType},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            verify=False,
        )
        r.raise_for_status()
    except Exception:
        flash("Failed to fetch the list of Cisco products! Please try again", "danger")
        return redirect(url_for("products.product"))
    else:
        return r.json().get("Cisco").get("products")
