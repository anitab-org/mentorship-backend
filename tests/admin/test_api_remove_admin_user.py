import unittest
from datetime import datetime, timedelta

from flask import json
from flask_restx import marshal

from app import messages
from app.api.models.admin import public_admin_user_api_model
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_utils import get_test_request_header
from tests.test_data import test_admin_user_2, test_admin_user_3
from http import HTTPStatus


class TestRemoveAdminUsersApi(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.admin_user_1 = UserModel(
            name=test_admin_user_2["name"],
            email=test_admin_user_2["email"],
            username=test_admin_user_2["username"],
            password=test_admin_user_2["password"],
            terms_and_conditions_checked=test_admin_user_2[
                "terms_and_conditions_checked"
            ],
        )

        self.admin_user_2 = UserModel(
            name=test_admin_user_3["name"],
            email=test_admin_user_3["email"],
            username=test_admin_user_3["username"],
            password=test_admin_user_3["password"],
            terms_and_conditions_checked=test_admin_user_3[
                "terms_and_conditions_checked"
            ],
        )

        # creating 3 admin users(first admin user created by basetestcase setup) and 1 normal user
        self.admin_user_1.is_email_verified = True
        self.admin_user_2.is_email_verified = True

        self.admin_user_1.is_admin = True
        self.admin_user_2.is_admin = True

        db.session.add(self.admin_user_1)
        db.session.add(self.admin_user_2)
        db.session.commit()

    def test_remove_self_admin_status_with_other_admins_api_resource_auth_admin(self):
        auth_header = get_test_request_header(self.admin_user_1.id)
        expected_response = messages.USER_ADMIN_STATUS_WAS_REVOKED
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.admin_user_1.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_remove_self_admin_status_when_only_admin_api_resource_auth_admin(self):
        # remove other admins
        auth_header = get_test_request_header(self.admin_user_1.id)
        expected_response = messages.USER_ADMIN_STATUS_WAS_REVOKED
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.admin_user_2.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

        # remove the admin that is always added for tests (id = 1)
        auth_header = get_test_request_header(self.admin_user_1.id)
        expected_response = messages.USER_ADMIN_STATUS_WAS_REVOKED
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": 1},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

        # remove self
        auth_header = get_test_request_header(self.admin_user_1.id)
        expected_response = messages.USER_CANNOT_REVOKE_ADMIN_STATUS
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.admin_user_1.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.FORBIDDEN, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_remove_admin_status_api_resource_auth_admin(self):
        auth_header = get_test_request_header(self.admin_user_1.id)
        expected_response = messages.USER_ADMIN_STATUS_WAS_REVOKED
        actual_response = self.client.post(
            "/admin/remove",
            json={"user_id": self.admin_user_2.id},
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
