import requests
from flask import flash, redirect, render_template, request, session, url_for
from markupsafe import escape

from psiapp import limiter
from psiapp.products import bp
from psiapp.products.forms import ProductSearchForm
from psiapp.products.utils import fetch_products
from psiapp.utils import fetch_data, paginate


# By Cisco Product Search Form Page
@bp.route("/search", methods=["GET", "POST"])
@limiter.exempt
def product(title="Cisco Products"):
    form = ProductSearchForm()
    products = fetch_products(prodType="CISCO")
    form.product.choices = products
    if form.is_submitted():
        product = escape(request.form.get("product").strip())
        return redirect(url_for("products.results", product=product))
    return render_template("product/form.html", title=title, form=form)


# By Cisco Product Search Results Page
@bp.get("")
def results():
    if not request.args.get("product", None, type=str):
        flash("A Cisco product is required!", "danger")
        return redirect(url_for(".product"))
    product = request.args.get("product", type=str)
    pageIndex = request.args.get("pageIndex", 1, type=int)
    pageSize = request.args.get("pageSize", 10, type=int)
    title = f"Search results for {product}"
    uri = "product?product={}&pageIndex={}&pageSize={}"
    try:
        res = fetch_data(
            uri=f"{uri.format(product, pageIndex, pageSize)}&productNames=false",
            access_token=session.get("access_token"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", "danger")
        return redirect(url_for(".product"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            flash(
                "Session expired! You are redirected here to refresh the session",
                "info",
            )
            return redirect(url_for("main.index"))
        if e.response.status_code in [404, 406]:
            flash(e.response.json().get("errorMessage"), "danger")
            return redirect(url_for(".product"))
        if e.response.status_code == 503:
            flash(
                "Service is currently unavailable from Cisco! Try again later", "danger"
            )
            return redirect(url_for(".product"))
        flash(str(e), "danger")
        return redirect(url_for(".product"))
    else:
        advisories = res.json().get("advisories")
        pagination = res.json().get("paging")
        paging = paginate(paging=pagination, pageIndex=pageIndex, pageSize=pageSize)
        total_count = paging.get("total_count")
        tnp = paging.get("tnp")  # total number of pages
        start = paging.get("start")
        end = paging.get("end")
        prev_url = pagination.get("prev")
        first_url = uri.format(product, 1, pageSize)
        next_url = pagination.get("next")
        last_url = uri.format(product, tnp, pageSize)
        flash(f"Page {pageIndex} of {tnp} - {title}", "success")
        return render_template(
            "product/results.html",
            title=title,
            advisories=advisories,
            product=product,
            pagination=pagination,
            prev_url=prev_url,
            first_url=first_url,
            next_url=next_url,
            last_url=last_url,
            total_count=total_count,
            tnp=tnp,
            start=start + 1,
            end=end,
        )
