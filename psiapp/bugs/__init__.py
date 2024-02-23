from flask import Blueprint

bp = Blueprint("bugs", __name__, template_folder="templates")

from psiapp.bugs import views
