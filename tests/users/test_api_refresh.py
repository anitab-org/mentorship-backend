import unittest
from datetime import timedelta

from flask import json

from app.database.sqlalchemy_extension import DB
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import USER1
from tests.test_utils import get_test_request_header


class TestUserRefreshApi(BaseTestCase):

    # User 1 which has email verified
    def setUp(self):
        super(TestUserRefreshApi, self).setUp()

        self.first_user = UserModel(
            name=USER1["name"],
            email=USER1["email"],
            username=USER1["username"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"]
        )
        self.first_user.is_email_verified = True

        DB.session.add(self.first_user)
        DB.session.commit()

    def test_user_refresh(self):
        with self.client:
            refresh_header = get_test_request_header(
                USER1["username"], refresh=True)
            response = self.client.post(
                "/refresh",
                headers=refresh_header,
                follow_redirects=True,
                content_type="application/json")

            self.assertIsNotNone(response.json.get("access_token"))
            self.assertIsNotNone(response.json.get("access_expiry"))
            self.assertEqual(2, len(response.json))
            self.assertEqual(200, response.status_code)

    def test_user_refresh_without_header(self):
        expected_response = {"message": "The authorization token is missing!"}
        actual_response = self.client.post("/refresh", follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_user_refresh_invalid_token(self):
        with self.client:
            refresh_token = "invalid_token"
            auth_header = {
                "Authorization": "Bearer {}".format(refresh_token)
            }
            expected_response = {"message": "The token is invalid!"}
            actual_response = self.client.post(
                "/refresh",
                headers=auth_header,
                follow_redirects=True,
                content_type="application/json")

            self.assertEqual(401, actual_response.status_code)
            self.assertEqual(
                expected_response, json.loads(
                    actual_response.data))

    def test_user_refresh_expired_token(self):
        auth_header = get_test_request_header(
            self.first_user.id, token_expiration_delta=timedelta(
                minutes=-5), refresh=True)
        expected_response = {
            "message": "The token has expired! Please, login again or refresh it."}
        actual_response = self.client.post(
            "/refresh",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json")

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
