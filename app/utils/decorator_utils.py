"""
This module is used to define decorators for the app
"""
from app import messages
from http import HTTPStatus
from app.database.models.user import UserModel


def email_verification_required(user_function):
    """
    This function is used to validate the
    input function i.e. user_function
    It will check if the user given as a
    parameter to user_function
    exists and have its email verified
    """

    def check_verification(*args, **kwargs):
        """
        Function to validate the input function ie user_function
        - It will return error 404 if user doesn't exist
        - It will return error 400 if user hasn't verified email

        Parameters:
        Function to be validated can have any type of argument
        - list
        - dict
        """

        if kwargs:
            user = UserModel.find_by_id(kwargs["user_id"])
        else:
            user = UserModel.find_by_id(args[0])

        # verify if user exists
        if user:
            if not user.is_email_verified:
                return messages.USER_HAS_NOT_VERIFIED_EMAIL_BEFORE_LOGIN, HTTPStatus.FORBIDDEN
            return user_function(*args, **kwargs)
        else:
            return messages.USER_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

    return check_verification
