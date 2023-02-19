from datetime import datetime

from flask import Blueprint

filters_bp = Blueprint("filters", __name__)


@filters_bp.app_template_filter(name="fromtimestamp")
def datectime(datetimestamp):
    return datetime.fromisoformat(datetimestamp).strftime("%Y-%b-%d")
