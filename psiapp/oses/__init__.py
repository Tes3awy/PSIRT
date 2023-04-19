from flask import Blueprint

bp = Blueprint("oses", __name__, url_prefix="/OSType", template_folder="templates")

from psiapp.oses import views
