from datetime import datetime, timedelta


def complete_remove_unverified_users_job():
    """
    This function iterates of all the unverified users and
    checks if email is not verified beyond a period of time.
    if True then user is removed, if False does nothing
    """
    VERIFICATION_TIME = timedelta(days = 20)
    from run import application
    with application.app_context():
        from app.database.models.user import UserModel
        unverified_users = UserModel.query.filter_by(is_email_verified = False)

        current_time = datetime.now()

        for user in unverified_users:
            register_time = datetime.fromtimestamp(user.registration_date)
            time_difference = current_time - register_time

            if time_difference > VERIFICATION_TIME:
                UserModel.delete_from_db(user)
