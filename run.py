from flask import Flask
from config import get_env_config


def create_app(config_filename):
    app = Flask(__name__)

    # setup application environment
    app.config.from_object(config_filename)
    app.url_map.strict_slashes = False

    from app.database.sqlalchemy_extension import DB

    DB.init_app(app)

    from app.api.jwt_extension import JWT

    JWT.init_app(app)

    from app.api.api_extension import API

    API.init_app(app)

    from app.api.mail_extension import MAIL

    MAIL.init_app(app)

    from app.schedulers.background_scheduler import init_scheduler

    init_scheduler()

    return app


application = create_app(get_env_config())  # pylint: disable=invalid-name


@application.before_first_request
def create_tables():
    from app.database.sqlalchemy_extension import DB

    DB.create_all()


if __name__ == "__main__":
    application.run(port=5000)
