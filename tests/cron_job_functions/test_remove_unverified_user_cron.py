import unittest
import time
from unittest.mock import patch

from app.database.sqlalchemy_extension import db
from app.schedulers.remove_unverified_user_cron_job import remove_unverified_user_job
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2, user3
from app.api.email_utils import EMAIL_VERIFICATION_TOKEN_TIME_TO_EXPIRE


class TestRemoveUnverifiedUserCronFunction(BaseTestCase):

    # Setup consists of adding 3 users into the database
    # User 1 is the verified user.
    # User 2 is the unverified user with verification token not yet expired.
    # User 3 is the unverified user with verification token expired.
    def setUp(self):
        super(TestRemoveUnverifiedUserCronFunction, self).setUp()

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.second_user = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )
        self.third_user = UserModel(
            name=user3['name'],
            email=user3['email'],
            username=user3['username'],
            password=user3['password'],
            terms_and_conditions_checked=user3['terms_and_conditions_checked']
        )

        current_time = time.time()
        self.first_user.is_email_verified = True
        self.third_user.registration_date = time.time() - EMAIL_VERIFICATION_TOKEN_TIME_TO_EXPIRE

        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.add(self.third_user)
        db.session.commit()

    def get_test_app(self):
        return self.app

    @patch('run.application', side_effect=get_test_app)
    def test_remove_unverified_users(self, get_test_app_fn):

        firstUser = UserModel.find_by_id(self.first_user.id)
        secondUser = UserModel.find_by_id(self.second_user.id)
        thirdUser = UserModel.find_by_id(self.third_user.id)

        self.assertIsNotNone(firstUser)
        self.assertIsNotNone(secondUser)
        self.assertIsNotNone(thirdUser)

        remove_unverified_user_job()

        firstUser = UserModel.find_by_id(self.first_user.id)
        secondUser = UserModel.find_by_id(self.second_user.id)
        thirdUser = UserModel.find_by_id(self.third_user.id)

        self.assertIsNotNone(firstUser)
        self.assertIsNotNone(secondUser)
        self.assertIsNone(thirdUser)


if __name__ == "__main__":
    unittest.main()
