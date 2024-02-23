from flask import Blueprint

bp = Blueprint("main", __name__, template_folder="templates", static_folder="static")

from psiapp.main import views
