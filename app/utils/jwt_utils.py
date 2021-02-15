from flask_jwt_extended import JWTManager
from app.api.dao.user import UserDAO
import os

"""
This module is used to modify the default behaviours of flask_jwt_extended
"""


def setup_jwt(application):
    jwt = JWTManager(application)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        return identity["userID"]

    """Since there is no way of knowing in the encode_key_loader 
    if we are returning the key for the refresh token or the 
    access token we can modify the value we pass as identity 
    to the create_access_token and create_refresh_token methods"""

    @jwt.encode_key_loader
    def custom_encode_key(identity):
        secret = os.environ["SECRET_KEY"]
        if identity["token_type"] == "access":
            return secret
        password_hash = UserDAO.get_user(identity["userID"]).password_hash
        return secret + password_hash

    @jwt.decode_key_loader
    def custom_dencode_key(jwt_payload):
        secret = os.environ["SECRET_KEY"]
        if jwt_payload["type"] == "access":
            return secret
        else:
            password_hash = UserDAO.get_user(jwt_payload["identity"]).password_hash
            return secret + password_hash
