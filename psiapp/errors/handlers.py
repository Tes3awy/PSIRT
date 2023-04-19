from flask import render_template
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    InternalServerError,
    NotFound,
    TooManyRequests,
    Unauthorized,
)

from psiapp.errors import bp


@bp.app_errorhandler(CSRFError)  # 400
@bp.app_errorhandler(BadRequest)  # 400
@bp.app_errorhandler(Unauthorized)  # 401
@bp.app_errorhandler(Forbidden)  # 403
@bp.app_errorhandler(NotFound)  # 404
@bp.app_errorhandler(TooManyRequests)  # 429
@bp.app_errorhandler(InternalServerError)  # 500
def handle_http_error(ex):
    return render_template("errors/error.html", title=ex.name, error=ex), ex.code
