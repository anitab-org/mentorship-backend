from flask_jwt_extended import JWTManager
from http import HTTPStatus
from app import messages
from app.api.api_extension import api
from app.database.models.token import TokenModel

jwt = JWTManager()

# This is needed for the error handlers to work with flask-restplus
jwt._set_error_handler_callbacks(api)


@jwt.expired_token_loader
def my_expired_token_callback():
    return messages.TOKEN_HAS_EXPIRED, HTTPStatus.UNAUTHORIZED


@jwt.invalid_token_loader
def my_invalid_token_callback(error_message):
    return messages.TOKEN_IS_INVALID, HTTPStatus.UNAUTHORIZED


@jwt.unauthorized_loader
def my_unauthorized_request_callback(error_message):
    return messages.AUTHORISATION_TOKEN_IS_MISSING, HTTPStatus.UNAUTHORIZED


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    jti = decoded_token['jti']
    token = TokenModel.query.filter_by(jti=jti).one()
    return token.revoked
        