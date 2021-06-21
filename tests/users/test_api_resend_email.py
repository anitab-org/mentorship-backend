import unittest

from flask import json

from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from tests.test_data import user1


class TestResendEmailApi(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.verified_user = UserModel(**user1)

        self.verified_user.is_email_verified = True
        self.verified_user.is_available = False
        db.session.add(self.verified_user)
        db.session.commit()

    # This function checks if the status code returns 409 for exisiting email
    def test_resend_email_user_already_verified(self):
        test_payload = {"email": self.verified_user.email}
        actual_response = self.client.post(
            "user/resend_email",
            follow_redirects=True,
            content_type="application/json",
            data=json.dumps(test_payload),
        )
        self.assertEqual(HTTP_STATUS.CONFLICT, actual_response.status_code)
        self.assertEqual(messages.USER_ALREADY_CONFIRMED_ACCOUNT, actual_response.json)


if __name__ == "__main__":
    unittest.main()
