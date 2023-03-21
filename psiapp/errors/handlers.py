from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    InternalServerError,
    NotFound,
    TooManyRequests,
    Unauthorized,
)

errors_bp = Blueprint("errors", __name__)

@errors_bp.app_errorhandler(CSRFError)
@errors_bp.app_errorhandler(BadRequest)
@errors_bp.app_errorhandler(Unauthorized)
@errors_bp.app_errorhandler(Forbidden)
@errors_bp.app_errorhandler(NotFound)
@errors_bp.app_errorhandler(TooManyRequests)
@errors_bp.app_errorhandler(InternalServerError)
def handle_http_error(error):
    return render_template("error.html", title=error.name, error=error), error.code
