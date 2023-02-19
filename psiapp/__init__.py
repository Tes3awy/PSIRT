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

from warnings import filterwarnings

from flask import Flask
from flask_compress import Compress
from flask_htmlmin import HTMLMIN
from flask_limiter import Limiter, util

from config import Config, ProductionConfig

filterwarnings(action="ignore", module="urllib3")  # Suppress HTTPS Warning

compress = Compress()
htmlmin = HTMLMIN()
limiter = Limiter(
    key_func=util.get_remote_address, default_limits=["30 per minute, 5 per second"]
)


def create_app(config_class=Config):  # Replace with ProductionConfig in Production
    app = Flask(__name__)
    app.config.from_object(obj=config_class)

    compress.init_app(app)
    htmlmin.init_app(app)
    limiter.init_app(app)

    from psiapp.bugs.views import bugs_bp
    from psiapp.cves.views import cves_bp
    from psiapp.errors.handlers import errors_bp
    from psiapp.filters.filters import filters_bp
    from psiapp.main.views import main_bp
    from psiapp.oses.views import oses_bp
    from psiapp.products.views import products_bp

    limiter.exempt(main_bp)
    limiter.exempt(errors_bp)

    app.register_blueprint(bugs_bp)
    app.register_blueprint(cves_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(filters_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(oses_bp)
    app.register_blueprint(products_bp)

    return app
