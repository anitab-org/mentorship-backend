from app.database.models.user import UserModel
from flask_jwt_extended import get_jwt_identity

def check_mail_confirmation(f):

    def wrapper(user_id,data):
        user = UserModel.find_by_id(user_id)
        if user.is_email_verified:
            return f(user_id, data)
        else:
            return {"message": "You have not confirmed your email."}, 400
    return wrapper
