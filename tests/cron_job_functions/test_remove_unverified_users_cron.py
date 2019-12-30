import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from app.database.sqlalchemy_extension import db
from app.schedulers.remove_unverified_users_cron_job import complete_remove_unverified_users_job
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2


class TestRemoveUnverifiedUsersCronFunction(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the unverified user
    # User 2 is the verified user
    # Registration date is 5 weeks before current date
    def setUp(self):
        super(TestRemoveUnverifiedUsersCronFunction, self).setUp()

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked'],
        )
        self.second_user = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )

        #set user 1 as unverified
        self.first_user.is_email_verified = False
        self.second_user.is_email_verified = True

        #set registration time
        self.now_datetime = datetime.now()
        self.past_date = self.now_datetime - timedelta(weeks=5)
        self.first_user.registration_date= self.past_date.timestamp()
        self.second_user.registration_date= self.past_date.timestamp()

        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.commit()

    def get_test_app(self):
        return self.app

    @patch('run.application', side_effect=get_test_app)
    def test_complete_mentorship_relations_accepted(self, get_test_app_fn):

        self.assertEqual(self.past_date.timestamp(), self.first_user.registration_date)
        self.assertEqual(self.past_date.timestamp(), self.second_user.registration_date)
        self.assertEqual(False, self.first_user.is_email_verified)
        self.assertEqual(True, self.second_user.is_email_verified)

        complete_remove_unverified_users_job()

        first_user=UserModel.find_by_id(self.first_user.id)
        second_user=UserModel.find_by_id(self.second_user.id)
        self.assertIsNone(first_user)
        self.assertIsNotNone(second_user)

if __name__ == "__main__":
    unittest.main()
