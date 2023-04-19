from flask import Blueprint

bp = Blueprint(
    "main",
    __name__,
    url_prefix="/main",
    template_folder="templates",
    static_folder="static",
)

from psiapp.main import views
