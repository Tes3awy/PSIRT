import requests
from flask import flash, redirect, render_template, request, session, url_for
from markupsafe import escape

from psiapp import limiter
from psiapp.oses import bp
from psiapp.oses.forms import OSVersionSearchForm
from psiapp.utils import fetch_data, paginate


# By OS-Version Search Form Page
@bp.route("/", methods=["GET", "POST"])
@limiter.exempt
def os(title="Search by OS-Version"):
    form = OSVersionSearchForm()
    if form.validate_on_submit():
        os_type = form.os_type.data
        version = form.version.data
        return redirect(
            url_for(".results", os_type=os_type, version=escape(version.strip()))
        )
    return render_template("os/form.html", title=title, form=form)


# By OS-Version Search Results Page
@bp.get("/<string:os_type>")
def results(os_type: str):
    if not request.args.get("version", None, type=str):
        flash("An OS version is required!", "danger")
        return redirect(url_for(".os"))
    pageIndex = request.args.get("pageIndex", 1, int)
    pageSize = request.args.get("pageSize", 10, int)
    version = escape(request.args.get("version").strip())
    title = f"Search results for {os_type.upper()} {version}"
    uri = "{}?version={}&pageIndex={:n}&pageSize={:n}"
    try:
        res = fetch_data(
            uri=f"OSType/{uri.format(os_type.lower(), version, pageIndex, pageSize)}&productNames=false",
            access_token=session.get("access_token"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", "danger")
        return redirect(url_for(".os"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            flash(
                "Session has expired! You are redirected to the Home page to refresh your session",
                "info",
            )
            return redirect(url_for("main.index"))
        if e.response.status_code in [404, 406]:
            flash(e.response.json().get("errorMessage"), "danger")
            return redirect(url_for(".os"))
        if e.response.status_code == 503:
            flash(
                "Service is currently unavailable from Cisco! Please try again later",
                "danger",
            )
            return redirect(url_for(".os"))
        flash(str(e), "danger")
        return redirect(url_for(".os"))
    else:
        advisories = res.json().get("advisories")
        paging = paginate(
            paging=res.json().get("paging"),
            pageIndex=pageIndex,
            pageSize=pageSize,
        )
        total_count = paging.get("total_count")
        tnp = paging.get("tnp")  # total number of pages
        start = paging.get("start")
        end = paging.get("end")
        prev_url = res.json().get("paging").get("prev")
        first_url = uri.format(os_type.lower(), version, 1, pageSize)
        next_url = res.json().get("paging").get("next")
        last_url = uri.format(os_type.lower(), version, tnp, pageSize)
        pagination = res.json().get("paging")
        flash(
            f"Page {pageIndex} of {tnp} - Search results for {os_type.upper()} {version}",
            "success",
        )
        return render_template(
            "os/results.html",
            title=title,
            os_type=os_type,
            version=version,
            advisories=advisories,
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
