import os
import sys

from datetime import timedelta

from flask import Flask
from flask_restplus import Api
from flask_jwt import JWT

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

#application.secret_key = 'SECRET_KEY'


# returns 'access_token'
jwt = JWT(application, authenticate, identity)
application.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300)
#application.config['JWT_AUTH_URL_RULE'] = '/login'  # POST /auth is created by JWT (default)


api = Api(
    app=application,
    title='Mentorship System API',
    version='1.0',
    description='API documentation for the backend of Mentorship System',
    #doc='/docs/'
)

@application.before_first_request
def create_tables():
    #db.drop_all()
    db.create_all()

# Adding namespaces
def add_namespaces():
    # called here to avoid circular imports
    from app.api.resources.user import users_ns as user_namespace
    api.add_namespace(user_namespace, path='/')


if __name__ == "__main__":
    add_namespaces()
    from app.database.db import db
    db.init_app(application)
    application.run(port=5000, debug=True)
