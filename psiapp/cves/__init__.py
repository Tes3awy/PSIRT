from flask import Blueprint

bp = Blueprint("cves", __name__, url_prefix="/cve", template_folder="templates")

from psiapp.cves import views
