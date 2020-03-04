import time
from datetime import datetime
from unittest.mock import patch

import config
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.schedulers.delete_unverified_users_cron_job import delete_unverified_users_job
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2, user3


class TestDeleteUnverifiedUsersCronFunction(BaseTestCase):
    def setUp(self):
        super(TestDeleteUnverifiedUsersCronFunction, self).setUp()

        self.verified_user = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        self.new_unverified_user = UserModel(
            name=user2["name"],
            email=user2["email"],
            username=user2["username"],
            password=user2["password"],
            terms_and_conditions_checked=user2["terms_and_conditions_checked"],
        )

        self.old_unverified_user = UserModel(
            name=user3["name"],
            email=user3["email"],
            username=user3["username"],
            password=user3["password"],
            terms_and_conditions_checked=user3["terms_and_conditions_checked"],
        )

        threshold = config.BaseConfig.UNVERIFIED_USER_THRESHOLD
        registration_timestamp = time.time() - threshold

        self.verified_user.is_email_verified = True
        self.old_unverified_user.registration_date = registration_timestamp

        db.session.add(self.verified_user)
        db.session.add(self.new_unverified_user)
        db.session.add(self.old_unverified_user)
        db.session.commit()

    def get_test_app(self):
        return self.app

    @patch("run.application", side_effect=get_test_app)
    def test_delete(self, get_test_app_fn):
        verified = UserModel.find_by_id(self.verified_user.id)
        new_unverified = UserModel.find_by_id(self.new_unverified_user.id)
        old_unverified = UserModel.find_by_id(self.old_unverified_user.id)

        self.assertEqual(self.verified_user, verified)
        self.assertEqual(self.new_unverified_user, new_unverified)
        self.assertEqual(self.old_unverified_user, old_unverified)

        delete_unverified_users_job()

        verified = UserModel.find_by_id(self.verified_user.id)
        new_unverified = UserModel.find_by_id(self.new_unverified_user.id)
        old_unverified = UserModel.find_by_id(self.old_unverified_user.id)

        self.assertEqual(self.verified_user, verified)
        self.assertEqual(self.new_unverified_user, new_unverified)
        self.assertIsNone(old_unverified)
