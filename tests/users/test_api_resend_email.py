import unittest

from flask import json

from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from tests.test_data import user1


class TestResendEmailApi(BaseTestCase):

    def setUp(self):
        super(TestResendEmailApi, self).setUp()

        self.verified_user = UserModel(
            name=user1["name"] + "Example",
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )

        self.verified_user.is_email_verified = True
        self.verified_user.is_available = False
        db.session.add(self.verified_user)
        db.session.commit()

    def test_user_error_code_conflict_for_resend_email(self):
        test_payload = {
            "email": self.verified_user.email
        }
        actual_response = self.client.post(
            "user/resend_email",
            follow_redirects=True,
            content_type="application/json",
            data=json.dumps(test_payload)
        )
        self.assertEqual(409, actual_response.status_code)


if __name__ == "__main__":
    unittest.main()