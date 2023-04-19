import requests
from flask import flash, redirect, url_for


def fetch_products(prodType: str = "CISCO") -> list[str]:
    try:
        r = requests.get(
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
        products = r.json().get("Cisco").get("products")
        return [product.get("productName") for product in products]
