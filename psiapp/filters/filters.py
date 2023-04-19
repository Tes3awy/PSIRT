from datetime import datetime

from psiapp.filters import bp


@bp.app_template_filter(name="fromtimestamp")
def datectime(datetimestamp: str):
    return datetime.fromisoformat(datetimestamp).strftime("%B %d, %Y %H:%M")
