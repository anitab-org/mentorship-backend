import os

from flask import Flask, jsonify
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from app.security import authenticate, identity
from datetime import datetime

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
    db.create_all()

# Adding namespaces
def add_namespaces():
    # called here to avoid circular imports
    from app.api.resources.user import users_ns as user_namespace
    api.add_namespace(user_namespace, path='/')
    from app.api.resources.admin import admin_ns as admin_namespace
    api.add_namespace(admin_namespace, path='/')
    from app.api.resources.mentorship_relation import mentorship_relation_ns as mentorship_namespace
    api.add_namespace(mentorship_namespace, path='/')


jwt = JWT(application, authenticate, identity)


@jwt.auth_response_handler
def custom_jwt_response_handler(access_token, identity):
    payload = jwt.jwt_payload_callback(identity)

    if 'exp' in payload:
        expiry = payload['exp']
    else:
        expiry = datetime.utcnow() + application.config.get('JWT_EXPIRATION_DELTA')

    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'expiry': expiry.timestamp()
    })


db = SQLAlchemy(application)


@application.before_first_request
def create_tables():
    # db.drop_all()
    db.create_all()


if __name__ == "__main__":
    add_namespaces()
    application.run(port=5000)
