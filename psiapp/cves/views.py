import requests
from flask import flash, redirect, render_template, request, session, url_for
from markupsafe import escape

from psiapp import limiter
from psiapp.cves import bp
from psiapp.cves.forms import CVESearchForm
from psiapp.utils import fetch_data


# CVE Search Form Page
@bp.route("/", methods=["GET", "POST"])
@limiter.exempt
def cve(title="CVE ID"):
    form = CVESearchForm()
    if form.validate_on_submit():
        cve_id = escape(form.cve_id.data.strip().upper())
        return redirect(url_for(".result", cve_id=cve_id))
    return render_template("cve/form.html", title=title, form=form)


# CVE Search Results Page
@bp.get("/result")
def result():
    if not request.args.get("cve_id", None, type=str):
        flash("A Cisco CVE ID is required!", "danger")
        return redirect(url_for(".cve"))
    cve_id = escape(request.args.get("cve_id").strip().upper())
    try:
        res = fetch_data(
            uri=f"cve/{cve_id}?productNames=true",
            access_token=session.get("access_token"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", "danger")
        return redirect(url_for(".cve"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            flash(
                "Session has expired! You are redirected to the Home page to refresh your session",
                "info",
            )
            return redirect(url_for("main.index"))
        if e.response.status_code == 404:
            flash(e.response.json().get("errorMessage"), "danger")
            return redirect(url_for(".cve"))
        if e.response.status_code == 406:
            flash(f"Unacceptable format of CVE ID {cve_id}!", "danger")
            return redirect(url_for(".cve"))
        flash(str(e), "danger")
        return redirect(url_for(".cve"))
    else:
        flash(f"Search result for {cve_id}", "success")
        advisories = res.json().get("advisories")
        return render_template("cve/result.html", title=cve_id, cve=advisories)
