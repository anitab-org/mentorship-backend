import os

from flask import Flask
from flask_restplus import Api
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy
from app.security import authenticate, identity

CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig'
}

application = Flask(__name__)

# setup application environment
flask_config_name = os.getenv('FLASK_CONFIG')
if flask_config_name is None:
    flask_config_name = 'development'

application.config.from_object(CONFIG_NAME_MAPPER[flask_config_name])

db = SQLAlchemy(application)
# returns 'access_token'
jwt = JWT(application, authenticate, identity)

api = Api(
    app=application,
    title='Mentorship System API',
    version='1.0',
    description='API documentation for the backend of Mentorship System',
    # doc='/docs/'
)


@application.before_first_request
def create_tables():
    from app.database.db_utils import db
    # db.drop_all()
    db.create_all()


# Adding namespaces
def add_namespaces():
    # called here to avoid circular imports
    from app.api.resources.user import users_ns as user_namespace
    from app.api.resources.admin import admin_ns as admin_namespace
    api.add_namespace(user_namespace, path='/')
    api.add_namespace(admin_namespace, path='/')


if __name__ == "__main__":
    add_namespaces()
    application.run(port=5000)
