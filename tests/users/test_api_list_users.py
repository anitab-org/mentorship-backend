import unittest
from flask import json
from flask_restplus import marshal
from app.api.models.user import PUBLIC_USER_API_MODEL
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import DB
from tests.base_test_case import BaseTestCase
from tests.test_utils import get_test_request_header
from tests.test_data import USER1, USER2


class TestListUsersApi(BaseTestCase):
    def setUp(self):
        super(TestListUsersApi, self).setUp()

        self.verified_user = UserModel(
            name=USER1["name"],
            email=USER1["email"],
            username=USER1["username"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        self.other_user = UserModel(
            name=USER2["name"],
            email=USER2["email"],
            username=USER2["username"],
            password=USER2["password"],
            terms_and_conditions_checked=USER2["terms_and_conditions_checked"],
        )

        self.verified_user.is_email_verified = True
        DB.session.add(self.verified_user)
        DB.session.add(self.other_user)
        DB.session.commit()

    def test_list_users_api_resource_non_auth(self):
        expected_response = {"message": "The authorization token is missing!"}
        actual_response = self.client.get("/users", follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_list_users_api_resource_auth(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = [
            marshal(self.verified_user, PUBLIC_USER_API_MODEL),
            marshal(self.other_user, PUBLIC_USER_API_MODEL),
        ]
        actual_response = self.client.get(
            "/users", follow_redirects=True, headers=auth_header
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_list_users_api_resource_verified_users(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = [
            marshal(self.verified_user, PUBLIC_USER_API_MODEL)
        ]
        actual_response = self.client.get(
            "/users/verified", follow_redirects=True, headers=auth_header
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
