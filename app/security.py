from werkzeug.security import safe_str_cmp
from app.database.models.user import UserModel


def authenticate(username_or_email, password):
    """
    The user can login with two options:
    -> username + password
    -> email + password
    """

    user = UserModel.find_by_username(username_or_email)

    if not user:
        user = UserModel.find_by_email(username_or_email)

    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
