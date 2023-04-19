from flask import Blueprint

bp = Blueprint("bugs", __name__, url_prefix="/bug", template_folder="templates")

from psiapp.bugs import views
