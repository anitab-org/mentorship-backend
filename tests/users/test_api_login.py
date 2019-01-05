import unittest

from flask import json

from app.database.sqlalchemy_extension import DB
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import USER1, USER2

# Testing User API resources
#
# TODO tests:
#     - lack of auth token
#     - invalid token
#     - expired token


class TestUserLoginApi(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 does not have email verified
    # User 2 has email verified
    def setUp(self):
        super(TestUserLoginApi, self).setUp()

        self.first_user = UserModel(
            name=USER1["name"],
            email=USER1["email"],
            username=USER1["username"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        self.second_user = UserModel(
            name=USER2["name"],
            email=USER2["email"],
            username=USER2["username"],
            password=USER2["password"],
            terms_and_conditions_checked=USER2["terms_and_conditions_checked"],
        )
        self.second_user.is_email_verified = True

        DB.session.add(self.first_user)
        DB.session.add(self.second_user)
        DB.session.commit()

    def test_user_login_non_verified_user(self):
        with self.client:
            response = self.client.post(
                "/login",
                data=json.dumps(
                    dict(
                        username=USER1["username"], password=USER1["password"]
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )

            self.assertIsNone(response.json.get("access_token"))
            self.assertIsNone(response.json.get("access_expiry"))
            self.assertIsNone(response.json.get("refresh_token"))
            self.assertIsNone(response.json.get("refresh_expiry"))
            self.assertEqual(1, len(response.json))
            self.assertEqual(
                "Please verify your email before login.",
                response.json.get("message", None),
            )
            self.assertEqual(403, response.status_code)

    def test_user_login_verified_user(self):
        with self.client:
            response = self.client.post(
                "/login",
                data=json.dumps(
                    dict(
                        username=USER2["username"], password=USER2["password"]
                    )
                ),
                follow_redirects=True,
                content_type="application/json"
            )
            self.assertIsNotNone(response.json.get("access_token"))
            self.assertIsNotNone(response.json.get("access_expiry"))
            self.assertIsNotNone(response.json.get("refresh_token"))
            self.assertIsNotNone(response.json.get("refresh_expiry"))
            self.assertEqual(4, len(response.json))
            self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
