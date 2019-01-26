from flask_jwt_extended import JWTManager
from app.api.api_extension import api
from app.utils.responses import ResponseMessages

jwt = JWTManager()

# This is needed for the error handlers to work with flask-restplus
jwt._set_error_handler_callbacks(api)


@jwt.expired_token_loader
def my_expired_token_callback():
    return {
               'message': ResponseMessages.TOKEN_HAS_EXPIRED
           }, 401


@jwt.invalid_token_loader
def my_invalid_token_callback(error_message):
    return {
               'message': ResponseMessages.TOKEN_IS_INVALID
           }, 401


@jwt.unauthorized_loader
def my_unauthorized_request_callback(error_message):
    return {
               'message': ResponseMessages.AUTHORISATION_TOKEN_IS_MISSING
           }, 401
