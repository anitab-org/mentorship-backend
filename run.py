
from flask import Flask, jsonify
from flask_jwt import JWT
from app.security import authenticate, identity
from datetime import datetime
from config import get_env_config

jwt = JWT(authentication_handler=authenticate, identity_handler=identity)


def create_app(config_filename):
    app = Flask(__name__)

    # setup application environment
    app.config.from_object(config_filename)
    app.url_map.strict_slashes = False

    from app.database import db
    db.init_app(app)

    jwt.init_app(app)

    from app.api import api
    api.init_app(app)

    return app


application = create_app(get_env_config())

@application.before_first_request
def create_tables():
    from app.database import db
    db.create_all()



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


if __name__ == "__main__":
    application.run(port=5000)
