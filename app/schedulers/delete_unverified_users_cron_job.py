import time

import config


def delete_unverified_users_job():
    """
    This function iterates of all the users and
    checks if the email is verified. If email is not verified
    then we are checking whether the specified threshold has passed
    since registration. If yes, user is deleted from the database.
    """

    from run import application

    with application.app_context():
        from app.database.models.user import UserModel

        unverified_users = list(
            UserModel.query.filter_by(is_email_verified=False).all()
        )
        threshold = config.BaseConfig.UNVERIFIED_USER_THRESHOLD
        for user in unverified_users:
            delta = time.time() - user.registration_date

            if delta > threshold:
                user.delete_from_db()
