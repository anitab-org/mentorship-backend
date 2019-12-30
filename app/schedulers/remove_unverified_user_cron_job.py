import time
from app.api.email_utils import EMAIL_VERIFICATION_TOKEN_TIME_TO_EXPIRE

def remove_unverified_user_job():
    """
    This function iterates over all the users and
    checks if a user has unverified email and
    the verification token of the user has expired.
    if True then the user is removed, if False does nothing.
    """
    from run import application
    with application.app_context():
        from app.database.models.user import UserModel
        all_users = UserModel.query.all()

        current_time = time.time()

        for user in all_users:
            # The date of removing unverified user, after the expiry of verification token.
            token_expiry_time = user.registration_date + EMAIL_VERIFICATION_TOKEN_TIME_TO_EXPIRE
            if user.is_email_verified == False and token_expiry_time < current_time:
                user.delete_from_db()
