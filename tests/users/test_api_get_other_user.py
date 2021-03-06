import unittest

from flask import json
from flask_restx import marshal
from http import HTTPStatus

from app import messages
from app.api.models.user import public_user_api_model
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2
from tests.test_utils import get_test_request_header


class TestnGetOtherUserApi(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.verified_user = UserModel(
            name=user1["name"] + "    Example",
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        self.other_user = UserModel(
            name=user2["name"],
            email=user2["email"],
            username=user2["username"],
            password=user2["password"],
            terms_and_conditions_checked=user2["terms_and_conditions_checked"],
        )

        self.verified_user.is_email_verified = True
        self.verified_user.is_available = False
        self.other_user.is_email_verified = True
        self.other_user.is_available = False
        db.session.add(self.verified_user)
        db.session.add(self.other_user)
        db.session.commit()

    def test_user_error_code_ok_for_other_user(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = marshal(self.verified_user, public_user_api_model)
        actual_response = self.client.get(
            f"/users/{self.verified_user.id}",
            follow_redirects=True,
            headers=auth_header,
        )
        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_user_invalid_user_id_for_other_user(self):
        auth_header = get_test_request_header(self.admin_user.id)
        actual_response = self.client.get(
            "/users/1234", follow_redirects=True, headers=auth_header
        )
        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertEqual(json.loads(actual_response.data), messages.USER_DOES_NOT_EXIST)


if __name__ == "__main__":
    unittest.main()
