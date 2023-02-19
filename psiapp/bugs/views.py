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
from psiapp.bugs.forms import BugSearchForm
from psiapp.utils import fetch_data

bugs_bp = Blueprint("bugs", __name__, url_prefix="/bug")


# Cisco Bug ID Search Form Page
@bugs_bp.route("/", methods=["GET", "POST"])
@limiter.exempt
def bug(title="Bug ID"):
    form = BugSearchForm()
    if form.validate_on_submit():
        bug_id = form.bug_id.data.strip()
        return redirect(url_for("bugs.result", bug_id=bug_id))
    return render_template("bug/form.html", title=title, form=form)


# Cisco Bug ID Result Page
@bugs_bp.route("/result", methods=["GET"])
def result():
    if not request.args.get("bug_id", None, type=str):
        flash("A Cisco bug ID is required!", category="danger")
        return redirect(url_for("bugs.bug"))
    bug_id = escape(request.args.get("bug_id").strip())
    try:
        res = fetch_data(
            uri=f"bugid/{bug_id}?productNames=false",
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
