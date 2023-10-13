import requests
from flask import current_app as app
from flask import flash, redirect, render_template, session, url_for

from psiapp.main import bp
from psiapp.main.utils import get_token


# Home Page
@bp.route("/", methods=["GET"])
def index(title="Home"):
    try:
        token = get_token(
            client_id=app.config.get("CLIENT_ID"),
            client_secret=app.config.get("CLIENT_SECRET"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", category="danger")
        return redirect(url_for("main.index"))
    except requests.exceptions.HTTPError as e:
        flash(e.response.json().get("errorMessage"), category="danger")
        return redirect(url_for("main.index"))
    else:
        session["access_token"] = token.get("access_token")
    return render_template("main/index.html", title=title)


# About Page
@bp.route("/about", methods=["GET"])
def about(title="About"):
    return render_template("main/about.html", title=title)
