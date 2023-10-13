import requests
from flask import flash, redirect, render_template, request, session, url_for
from markupsafe import escape

from psiapp import limiter
from psiapp.utils import fetch_data

from psiapp.bugs import bp
from psiapp.bugs.forms import BugSearchForm


# Cisco Bug ID Search Form Page
@bp.route("/", methods=["GET", "POST"])
@limiter.exempt
def bug(title="Bug ID"):
    form = BugSearchForm()
    if form.validate_on_submit():
        bug_id = form.bug_id.data.strip()
        return redirect(url_for("bugs.result", bug_id=bug_id))
    return render_template("bug/form.html", title=title, form=form)


# Cisco Bug ID Result Page
@bp.route("/result", methods=["GET"])
def result():
    if not request.args.get("bug_id", None, type=str):
        flash("A Cisco bug ID is required!", category="danger")
        return redirect(url_for("bugs.bug"))
    bug_id = escape(request.args.get("bug_id").strip())
    try:
        res = fetch_data(
            uri=f"bugid/{bug_id}?productNames=true",
            access_token=session.get("access_token"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", category="danger")
        return redirect(url_for("bugs.bug"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            flash(
                "Session has expired! You are redirected here to refresh your session",
                "info",
            )
            return redirect(url_for("main.index"))
        if e.response.status_code == 404:
            flash(
                f"{e.response.json().get('errorCode')} - {e.response.json().get('errorMessage')} for {bug_id}. Go to <a class='link' href='//bst.cloudapps.cisco.com/bugsearch/bug/{bug_id}' target='_blank' rel='noopener noreferrer'>https://bst.cloudapps.cisco.com/bugsearch/bug/{bug_id}</a>",
                category="warning",
            )
            return redirect(url_for("bugs.bug"))
        if e.response.status_code == 503:
            flash(
                "The service is currently unavailable from Cisco! Please try again later",
                category="danger",
            )
            return redirect(url_for("bugs.bug"))
        flash(str(e), category="danger")
        return redirect(url_for("bugs.bug"))
    else:
        flash(f"Search result for {bug_id}", category="success")
        advisories = res.json().get("advisories")
        return render_template("bug/result.html", title=bug_id, bug=advisories)
