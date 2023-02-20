import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from markupsafe import escape

from psiapp import limiter
from psiapp.oses.forms import OSVersionSearchForm
from psiapp.utils import fetch_data, get_pagination

oses_bp = Blueprint("oses", __name__, url_prefix="/OSType")


# By OS-Version Search Form Page
@oses_bp.route("/", methods=["GET", "POST"])
@limiter.exempt
def os(title="Search by OS-Version"):
    form = OSVersionSearchForm()
    if form.validate_on_submit():
        os = form.os.data
        version = escape(form.version.data.strip())
        return redirect(url_for("oses.results", os=os, version=version))
    return render_template("os/form.html", title=title, form=form)


# By OS-Version Search Results Page
@oses_bp.route("/<string:os>", methods=["GET"])
def results(os: str):
    if not request.args.get("version", None, type=str):
        flash("An OS version is required!", category="danger")
        return redirect(url_for("oses.os"))
    pageIndex = request.args.get("pageIndex", 1, int)
    pageSize = request.args.get("pageSize", 10, int)
    version = escape(request.args.get("version").strip())
    title = f"Search results for {os.upper()} {version}"
    try:
        res = fetch_data(
            uri=f"OSType/{os.lower()}?version={version}&pageIndex={pageIndex}&pageSize={pageSize}&productNames=false",
            access_token=session.get("access_token"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", category="danger")
        return redirect(url_for("oses.os"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            flash(
                "Session has expired! You are redirected here to refresh your session",
                category="info",
            )
            return redirect(url_for("main.index"))
        if e.response.status_code in [404, 406]:
            flash(
                f"{e.response.json().get('errorCode')} - {e.response.json().get('errorMessage')}",
                category="warning" if e.response.status_code == 404 else "danger",
            )
            return redirect(url_for("oses.os"))
        if e.response.status_code == 503:
            flash(
                "Service is currently unavailable from Cisco! Please try again later",
                category="danger",
            )
            return redirect(url_for("oses.os"))
        flash(str(e), category="danger")
        return redirect(url_for("oses.os"))
    else:
        advisories = res.json().get("advisories")
        pagination = get_pagination(
            paging=res.json().get("paging"), pageIndex=pageIndex
        )
        total_count = pagination.get("total_count")
        tnp = pagination.get("tnp")  # total number of pages
        start = pagination.get("start")
        end = pagination.get("end")
        pagination = res.json().get("paging")
        flash(
            f"{pageIndex}/{tnp} - Search results for {os.upper()} {version}",
            "success",
        )
        return render_template(
            "os/results.html",
            title=title,
            os=os,
            version=version,
            advisories=advisories,
            pagination=pagination,
            total_count=total_count,
            tnp=tnp,
            start=start + 1,
            end=end,
        )
