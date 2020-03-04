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
            filter(lambda user: not user.is_email_verified, UserModel.query.all())
        )

        for user in unverified_users:
            threshold = config.BaseConfig.UNVERIFIED_USER_THRESHOLD
            delta = time.time() - user.registration_date

            if delta > threshold:
                user.delete_from_db()
