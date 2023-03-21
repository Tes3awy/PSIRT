import requests
from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, session, url_for

from psiapp.main.utils import get_token

main_bp = Blueprint("main", __name__)


# Home Page
@main_bp.route("/home", methods=["GET"])
@main_bp.route("/", methods=["GET"])
def index(title="Home"):
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
def about(title="About"):
    return render_template("about.html", title=title)
