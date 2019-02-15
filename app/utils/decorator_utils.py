"""
This module is used to define decorators for the app
"""
from app.database.models.user import UserModel


# definition of decorator to validate user
def user_validation(user_function):
    """
    This function is used to validate the input function i.e. user_function
    It will check if the user given as a parameter to user_function
    exists and have its email verified.
    """

    # function to validate the input function i.e. user_function
    def validator(*args, **kwargs):

        #  check if the given paramenters are in form of dict (to get user_id)
        if kwargs:
            # if parameters are given in form of dict
            user = UserModel.find_by_id(kwargs['user_id'])
        else:
            # if parameters are given as args
            user = UserModel.find_by_id(args[0])
        # verify if user exists
        if user:
            # verify if user has verified his/her email
            if user.is_email_verified:
                pass
            else:
                return {'message': 'You have not confirmed your email.'}, 400
            return user_function(*args, **kwargs)
        else:
            return {'message': 'User does not exist.'}, 404

    return validator
