import unittest
from http import HTTPStatus

from flask import json

from app import messages
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db

from tests.base_test_case import BaseTestCase
from tests.test_data import user1, test_admin_user_2
from tests.test_utils import get_test_request_header


class TestRevokingAdminRoleApi(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.second_admin_user = UserModel(
            name=test_admin_user_2["name"],
            email=test_admin_user_2["email"],
            username=test_admin_user_2["username"],
            password=test_admin_user_2["password"],
            terms_and_conditions_checked=test_admin_user_2[
                "terms_and_conditions_checked"
            ],
        )

        self.non_admin_user = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )

        self.second_admin_user.is_email_verified = True
        self.non_admin_user.is_email_verified = True

        # two admin user and one non-admin user
        self.second_admin_user.is_admin = True
        self.non_admin_user.is_admin = False

        db.session.add(self.second_admin_user)
        db.session.add(self.non_admin_user)
        db.session.commit()

    def test_revoke_admin_role_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.second_admin_user.id},
            follow_redirects=True,
        )

        self.assertEqual(HTTPStatus.UNAUTHORIZED, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_revoke_self_admin_role_not_the_only_user_api_resource_auth(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.USER_ADMIN_STATUS_WAS_REVOKED
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.admin_user.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_revoke_self_admin_role_the_only_user_api_resource_auth(self):
        # revoke other admins to make the user the only admin
        self.second_admin_user.is_admin = False
        db.session.commit()

        # revoke self admin status
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.USER_CANNOT_REVOKE_ADMIN_STATUS
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.admin_user.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.FORBIDDEN, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_non_admin_user_revoke_admin_role_api_resource_auth(self):
        auth_header = get_test_request_header(self.non_admin_user.id)
        expected_response = messages.USER_REVOKE_NOT_ADMIN
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.second_admin_user.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.FORBIDDEN, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_revoke_admin_role_from_other_admin_user_api_resource_auth(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.USER_ADMIN_STATUS_WAS_REVOKED
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.second_admin_user.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_revoke_admin_role_from_non_admin_user_api_resource_auth(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.USER_IS_NOT_AN_ADMIN
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.non_admin_user.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_revoke_admin_role_from_non_existent_user_api_resource_auth(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.USER_DOES_NOT_EXIST
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": 0},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
