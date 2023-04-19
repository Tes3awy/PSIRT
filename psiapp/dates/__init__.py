from flask import Blueprint

bp = Blueprint("dates", __name__, template_folder="templates")

from psiapp.dates import views
