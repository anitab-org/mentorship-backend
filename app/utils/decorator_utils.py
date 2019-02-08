from app.database.models.user import UserModel


def check_mail_confirmation(func_to_validate):

    def to_validate_user(user_id, data):
        user = UserModel.find_by_id(user_id)
        if user.is_email_verified:
            return func_to_validate(user_id, data)
        else:
            return {"message": "You have not confirmed your email."}, 400
    return to_validate_user
