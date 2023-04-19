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

    from psiapp.bugs.views import bp as bugs_bp

    app.register_blueprint(bugs_bp)

    from psiapp.cves.views import bp as cves_bp

    app.register_blueprint(cves_bp)

    from psiapp.dates.views import bp as dates_bp

    app.register_blueprint(dates_bp)

    from psiapp.errors.handlers import bp as errors_bp

    app.register_blueprint(errors_bp)
    limiter.exempt(errors_bp)

    from psiapp.filters.filters import bp as filters_bp

    app.register_blueprint(filters_bp)
    limiter.exempt(filters_bp)

    from psiapp.main.views import bp as main_bp

    app.register_blueprint(main_bp)
    limiter.exempt(main_bp)

    from psiapp.oses.views import bp as oses_bp

    app.register_blueprint(oses_bp)

    from psiapp.products.views import bp as products_bp

    app.register_blueprint(products_bp)

    return app
