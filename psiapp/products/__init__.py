from flask import Blueprint

bp = Blueprint(
    "products", __name__, template_folder="templates", static_folder="static"
)

from psiapp.products import views
