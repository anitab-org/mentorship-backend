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
from tests.test_data import user1, test_admin_user, test_admin_user_2, test_admin_user_3
from http import HTTPStatus


class TestListAdminUsersApi(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.admin_user_2 = UserModel(
            name=test_admin_user_2["name"],
            email=test_admin_user_2["email"],
            username=test_admin_user_2["username"],
            password=test_admin_user_2["password"],
            terms_and_conditions_checked=test_admin_user_2[
                "terms_and_conditions_checked"
            ],
        )

        self.admin_user_3 = UserModel(
            name=test_admin_user_3["name"],
            email=test_admin_user_3["email"],
            username=test_admin_user_3["username"],
            password=test_admin_user_3["password"],
            terms_and_conditions_checked=test_admin_user_3[
                "terms_and_conditions_checked"
            ],
        )

        self.normal_user_1 = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )

        # creating 3 admin users(first admin user created by basetestcase setup) and 1 normal user
        self.admin_user_2.is_email_verified = True
        self.admin_user_3.is_email_verified = True
        self.normal_user_1.is_email_verified = True

        self.admin_user_2.is_admin = True
        self.admin_user_3.is_admin = True
        self.normal_user_1.is_admin = False

        db.session.add(self.admin_user_2)
        db.session.add(self.admin_user_3)
        db.session.add(self.normal_user_1)
        db.session.commit()

    """
    Test for api call from logged out users
    """

    def test_list_admin_users_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.get("/admins")

        self.assertEqual(HTTPStatus.UNAUTHORIZED, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    """
    Test for api call from admin users
    """

    def test_list_admin_users_api_resource_auth_admin(self):
        auth_header = get_test_request_header(self.admin_user_2.id)
        expected_response = [
            marshal(self.admin_user, public_admin_user_api_model),
            marshal(self.admin_user_3, public_admin_user_api_model),
        ]
        actual_response = self.client.get(
            "/admins", follow_redirects=True, headers=auth_header
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    """
    Test for api call from users who are not admins
    """

    def test_list_admin_users_api_resource_auth_not_admin(self):
        auth_header = get_test_request_header(self.normal_user_1.id)
        expected_response = messages.USER_IS_NOT_AN_ADMIN
        actual_response = self.client.get(
            "/admins", follow_redirects=True, headers=auth_header
        )

        # import pdb; pdb.set_trace()
        self.assertEqual(HTTPStatus.FORBIDDEN, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
