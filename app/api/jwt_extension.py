from flask_jwt_extended import JWTManager
from app.api.api_extension import API

JWT = JWTManager()

# This is needed for the error handlers to work with flask-restplus
# pylint: disable=unused-argument
JWT._set_error_handler_callbacks(API)  # pylint: disable=protected-access


@JWT.expired_token_loader
def my_expired_token_callback():
    return {
        "message": "The token has expired! Please, login again or refresh it."
    }, 401


@JWT.invalid_token_loader
def my_invalid_token_callback(error_message):
    return {"message": "The token is invalid!"}, 401


@JWT.unauthorized_loader
def my_unauthorized_request_callback(error_message):
    return {"message": "The authorization token is missing!"}, 401
