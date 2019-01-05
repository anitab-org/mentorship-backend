import unittest
from datetime import timedelta

from flask import json
from flask_restplus import marshal

from app.api.models.user import FULL_USER_API_MODEL
from app.database.sqlalchemy_extension import DB
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import USER1
from tests.test_utils import get_test_request_header


class TestProtectedApi(BaseTestCase):

    # User 1 which has email verified
    def setUp(self):
        super(TestProtectedApi, self).setUp()

        self.first_user = UserModel(
            name=USER1["name"],
            email=USER1["email"],
            username=USER1["username"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        self.first_user.is_email_verified = True

        DB.session.add(self.first_user)
        DB.session.commit()

    def test_user_profile_with_header_api(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = marshal(self.first_user, FULL_USER_API_MODEL)
        actual_response = self.client.get(
            "/user", follow_redirects=True, headers=auth_header
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_user_profile_without_header_api(self):
        expected_response = {"message": "The authorization token is missing!"}
        actual_response = self.client.get("/user", follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_user_profile_incomplete_token_api(self):
        access_token = "invalid_token"
        auth_header = {"Authorization": "Bearer {}".format(access_token)}
        expected_response = {"message": "The token is invalid!"}
        actual_response = self.client.get(
            "/user", follow_redirects=True, headers=auth_header
        )

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_user_profile_with_token_expired_api(self):
        auth_header = get_test_request_header(
            self.first_user.id, token_expiration_delta=timedelta(minutes=-5)
        )
        expected_response = {
            "message": "The token has expired! Please, login again or refresh it."}
        actual_response = self.client.get(
            "/user", follow_redirects=True, headers=auth_header
        )

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
