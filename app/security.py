from app.utils.email_utils import is_email_valid


def authenticate(username_or_email, password):
    """
    The user can login with two options:
    -> username + password
    -> email + password
    """
    from app.database.models.user import UserModel

    if is_email_valid(username_or_email):
        user = UserModel.find_by_email(username_or_email)
    else:
        user = UserModel.find_by_username(username_or_email)

    if user and user.check_password(password):
        return user


def identity(payload):
    from app.database.models.user import UserModel
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
