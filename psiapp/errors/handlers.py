"""Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
            https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError

errors_bp = Blueprint("errors", __name__)


# Error 400 Page (Bad Request)
@errors_bp.app_errorhandler(CSRFError)
def error_400(e):
    return render_template("errors/400.html", title=str(e.code), e=e), 400


# Error 403 Page (Forbidden)
@errors_bp.app_errorhandler(403)
def error_403(e):
    return render_template("errors/403.html", title=str(e.code), e=e), 403


# Error 404 Page (Page Not Found)
@errors_bp.app_errorhandler(404)
def error_404(e):
    return render_template("errors/404.html", title=str(e.code), e=e), 404


# Error 429 Page (Rate Limit Exceeded)
@errors_bp.app_errorhandler(429)
def error_429(e):
    return render_template("errors/429.html", title=str(e.code), e=e), 429


# Error 500 Page (Internal Server Error)
@errors_bp.app_errorhandler(500)
def error_500(e):
    return render_template("errors/500.html", title=str(e.code), e=e), 500
