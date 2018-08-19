from flask_jwt_extended import create_access_token


def get_test_request_header(user_identity, token_expiration_delta=None):
    """
    This function returns the header needed to access auth protected
    endpoints
    :param token_expiration_delta: time for the token to expire
    :param user_identity: identifier of the user
    :return: header dict with Authorization field
    """
    access_token = create_access_token(identity=user_identity, expires_delta=token_expiration_delta)
    header = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    return header
