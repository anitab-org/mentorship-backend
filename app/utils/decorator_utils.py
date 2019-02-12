from app.database.models.user import UserModel


def user_validation(user_function):

    def validator(*args, **kwargs):

        if len(kwargs) != 0:
            user = UserModel.find_by_id(kwargs['user_id'])
        else:
            user = UserModel.find_by_id(args[0])
        if user:
            if user.is_email_verified:
                return user_function(*args, **kwargs)
            else:
                return {'message': 'You have not confirmed your email.'}, 400
        else:
            return {'message': 'User does not exist.'}, 404

    return validator
