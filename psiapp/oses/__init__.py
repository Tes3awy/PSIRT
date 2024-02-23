from flask import Blueprint

bp = Blueprint("oses", __name__, template_folder="templates")

from psiapp.oses import views
