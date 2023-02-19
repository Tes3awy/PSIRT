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
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from markupsafe import escape

from psiapp import limiter
from psiapp.products.forms import ProductSearchForm
from psiapp.products.utils import fetch_products
from psiapp.utils import fetch_data, get_pagination

products_bp = Blueprint("products", __name__, url_prefix="/product")


# By Cisco Product Search Form Page
@products_bp.route("/search", methods=["GET", "POST"])
@limiter.exempt
def product(title="Cisco Products"):
    form = ProductSearchForm()
    products = fetch_products(prodType="CISCO")
    form.product.choices = [product.get("productName") for product in products]
    if form.is_submitted():
        product = escape(request.form.get("product").strip())
        return redirect(url_for("products.results", product=product))
    return render_template("product/form.html", title=title, form=form)


# By Cisco Product Search Results Page
@products_bp.route("/result", methods=["GET"])
def results():
    if not request.args.get("product", None, type=str):
        flash("A Cisco product is required!", category="danger")
        return redirect(url_for("products.product"))
    product = request.args.get("product", type=str)
    pageIndex = request.args.get("pageIndex", 1, type=int)
    pageSize = request.args.get("pageSize", 10, type=int)
    if "?pageIndex" in product:
        product, pageIndex = product.split(sep="?")
        _, pageIndex = pageIndex.split(sep="=")
    uri = f"product?product={product}&pageIndex={pageIndex}&pageSize={pageSize}&productNames=false"
    try:
        res = fetch_data(uri=uri, access_token=session.get("access_token"))
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", category="danger")
        return redirect(url_for("products.product"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            flash(
                "Session expired! You are redirected here to refresh the session",
                "info",
            )
            return redirect(url_for("main.index"))
        if e.response.status_code in [404, 406]:
            flash(
                f"{e.response.json().get('errorCode')} - {e.response.json().get('errorMessage')}",
                category="danger",
            )
            return redirect(url_for("products.product"))
        if e.response.status_code == 503:
            flash(
                "Service is currently unavailable from Cisco! Try again later", "danger"
            )
            return redirect(url_for("products.product"))
        flash(str(e), category="danger")
        return redirect(url_for("products.product"))
    else:
        advisories = res.json().get("advisories")
        pagination = get_pagination(
            paging=res.json().get("paging"), pageIndex=int(pageIndex)
        )
        total_count = pagination.get("total_count")
        tnp = pagination.get("tnp")  # total number of pages
        start = pagination.get("start")
        end = pagination.get("end")
        pagination = res.json().get("paging")
        flash(f"{pageIndex}/{tnp} - Search results for {product}", "success")
        return render_template(
            "product/results.html",
            title=f"Search results for {product}",
            advisories=advisories,
            product=product,
            pagination=pagination,
            total_count=total_count,
            tnp=tnp,
            start=start + 1,
            end=end,
        )
