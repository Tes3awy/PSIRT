from flask import Blueprint

bp = Blueprint(
    "products",
    __name__,
    url_prefix="/product",
    template_folder="templates",
    static_folder="static",
)

from psiapp.products import views
