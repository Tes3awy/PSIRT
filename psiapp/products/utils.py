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
