import requests
from flask import current_app, flash, redirect, render_template, session, url_for

from psiapp.main import bp
from psiapp.main.utils import get_token


# Home Page
@bp.get("/")
def index(title="Home"):
    try:
        token = get_token(
            client_id=current_app.config.get("CLIENT_ID"),
            client_secret=current_app.config.get("CLIENT_SECRET"),
        )
    except requests.exceptions.ConnectionError as e:
        flash("Connection Error! Failed to establish a connection", "danger")
        return redirect(url_for(".index"))
    except requests.exceptions.HTTPError as e:
        flash(e.response.json().get("errorMessage"), "danger")
        return redirect(url_for(".index"))
    else:
        session["access_token"] = token.get("access_token")
    return render_template("main/index.html", title=title)


# About Page
@bp.get("/about")
def about(title="About"):
    return render_template("main/about.html", title=title)
