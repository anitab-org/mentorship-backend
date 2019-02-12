from app.database.models.user import UserModel


def check_mail_confirmation(func_to_validate):

    def to_validate_user(*args, **kwargs):

        if len(kwargs) != 0:
            user = UserModel.find_by_id(kwargs['user_id'])
        else:
            user = UserModel.find_by_id(args[0])
        if user:
            if user.is_email_verified:
                return func_to_validate(*args, **kwargs)
            else:
                return {'message': 'You have not confirmed your email.'}, 200
        else:
            return {'message': 'User does not exist.'}, 404

    return to_validate_user
