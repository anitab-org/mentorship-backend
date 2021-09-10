import unittest

from flask import json
from http import HTTPStatus
from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.test_data import user1, user2, user3
from tests.test_utils import get_test_request_header


class TestFilterUsersBySkill(BaseTestCase):
    def setUp(self):
        super().setUp()
        

        # Insert data of the first entry
        self.first_user = UserModel(**user1)
        self.first_user.is_email_verified = True
        self.first_user.skills = "Problem Solving"

        db.session.add(self.first_user)
        db.session.commit()

        # Insert data of the second entry
        self.second_user = UserModel(**user2)
        self.second_user.is_email_verified = True
        self.second_user.skills = "Problem Solving"

        db.session.add(self.second_user)
        db.session.commit()

        # Insert data of the third entry
        self.third_user = UserModel(**user3)
        self.third_user.is_email_verified = True
        self.third_user.skills = "Critical thinking"

        db.session.add(self.third_user)
        db.session.commit()

    def test_filter_users_by_skill_problem_solving(self):

        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = "Problem Solving"

        actual_response = self.client.get(
            "/users/verified?skills=Problem Solving",
            headers=auth_header,
            content_type="application/json",
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)

        for data in json.loads(actual_response.data):
            self.assertEqual(expected_response, data["skills"])

    def test_filter_users_by_skill_critical(self):

        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = "Critical thinking"

        actual_response = self.client.get(
            "/users/verified?skills=Critical thinking",
            headers=auth_header,
            content_type="application/json",
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)

        for data in json.loads(actual_response.data):
            self.assertEqual(expected_response, data["skills"])


if __name__ == "__main__":
    unittest.main()
