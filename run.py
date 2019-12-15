from dotenv import load_dotenv
from flask import Flask

import cli.admin
import cli.database
import cli.mentorship_relation
import cli.task
import cli.user
from app.database.sqlalchemy_extension import db
from config import get_env_config

load_dotenv(verbose=True)


def create_app(config_filename):
    app = Flask(__name__)

    # setup application environment
    app.config.from_object(config_filename)
    app.url_map.strict_slashes = False

    db.init_app(app)

    from app.api.jwt_extension import jwt
    jwt.init_app(app)

    from app.api.api_extension import api
    api.init_app(app)

    from app.api.mail_extension import mail
    mail.init_app(app)

    from app.schedulers.background_scheduler import init_scheduler
    init_scheduler()

    return app


application = create_app(get_env_config())


@application.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    application.run(port=5000)

application.register_blueprint(cli.database.blueprint)
application.register_blueprint(cli.user.blueprint)
application.register_blueprint(cli.admin.blueprint)
application.register_blueprint(cli.mentorship_relation.blueprint)
application.register_blueprint(cli.task.blueprint)
