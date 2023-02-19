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
from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, session, url_for

from psiapp.main.utils import get_token

main_bp = Blueprint("main", __name__)


# Home Page
@main_bp.route("/home", methods=["GET"])
@main_bp.route("/", methods=["GET"])
def index(title="Home Page"):
    try:
        token = get_token(
            client_id=app.config["CLIENT_ID"], client_secret=app.config["CLIENT_SECRET"]
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", category="danger")
        return redirect(url_for("main.index"))
    except requests.exceptions.HTTPError as e:
        flash(e.response.json().get("errorMessage"), category="danger")
        return redirect(url_for("main.index"))
    else:
        session["access_token"] = token.get("access_token")
    return render_template("index.html", title=title)


# About Page
@main_bp.route("/faq", methods=["GET"])
@main_bp.route("/about", methods=["GET"])
def about(title="About Page"):
    return render_template("about.html", title=title)
