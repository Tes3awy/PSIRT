import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from markupsafe import escape

from psiapp import limiter
from psiapp.cves.forms import CVESearchForm
from psiapp.utils import fetch_data

cves_bp = Blueprint("cves", __name__, url_prefix="/cve")


# CVE Search Form Page
@cves_bp.route("/", methods=["GET", "POST"])
@limiter.exempt
def cve(title="CVE ID"):
    form = CVESearchForm()
    if form.validate_on_submit():
        cve_id = escape(form.cve_id.data.strip().upper())
        return redirect(url_for("cves.result", cve_id=cve_id))
    return render_template("cve/form.html", title=title, form=form)


# CVE Search Results Page
@cves_bp.route("/result", methods=["GET"])
def result():
    if not request.args.get("cve_id", None, type=str):
        flash("A Cisco CVE ID is required!", category="danger")
        return redirect(url_for("cves.cve"))
    cve_id = escape(request.args.get("cve_id").strip().upper())
    try:
        res = fetch_data(
            uri=f"cve/{cve_id}?productNames=false",
            access_token=session.get("access_token"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", category="danger")
        return redirect(url_for("cves.cve"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            flash(
                "Session has expired! You are redirected here to refresh your session",
                "info",
            )
            return redirect(url_for("main.index"))
        if e.response.status_code == 404:
            flash(f"No result found matching {cve_id}! Check typos", "warning")
            return redirect(url_for("cves.cve"))
        if e.response.status_code == 406:
            flash(f"Unacceptable format of CVE ID {cve_id}!", "danger")
            return redirect(url_for("cves.cve"))
        flash(str(e), category="danger")
        return redirect(url_for("cves.cve"))
    else:
        flash(f"Search result for {cve_id}", "success")
        advisories = res.json().get("advisories")
        return render_template("cve/result.html", title=cve_id, cve=advisories)
