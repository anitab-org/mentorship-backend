import unittest

from flask import json
from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.test_data import user1, user2, user3
from tests.test_utils import get_test_request_header


class FilterUsersBySkill(BaseTestCase):
    def insert_entries_in_database(self):

        # Insert data of the first entry
        self.first_user = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        self.first_user.is_email_verified = True
        self.first_user.skills = "Problem Solving"

        db.session.add(self.first_user)
        db.session.commit()

        # Insert data of the second entry
        self.second_user = UserModel(
            name=user2["name"],
            email=user2["email"],
            username=user2["username"],
            password=user2["password"],
            terms_and_conditions_checked=user2["terms_and_conditions_checked"],
        )
        self.second_user.is_email_verified = True
        self.second_user.skills = "Problem Solving"

        db.session.add(self.second_user)
        db.session.commit()

        # Insert data of the third entry
        self.third_user = UserModel(
            name=user3["name"],
            email=user3["email"],
            username=user3["username"],
            password=user3["password"],
            terms_and_conditions_checked=user3["terms_and_conditions_checked"],
        )
        self.third_user.is_email_verified = True
        self.third_user.skills = "Critical thinking"

        db.session.add(self.third_user)
        db.session.commit()

    def test_case_1(self):
        self.insert_entries_in_database()

        auth_header = get_test_request_header(self.admin_user.id)
        expected_response_1 = "Problem Solving"

        actual_response_1 = self.client.get(
            "/users/verified?skills=Problem Solving",
            headers=auth_header,
            content_type="application/json",
        )

        for data in json.loads(actual_response_1.data):
            self.assertEqual(expected_response_1, data["skills"])

    def test_case_2(self):
        self.insert_entries_in_database()

        auth_header = get_test_request_header(self.admin_user.id)
        expected_response_2 = "Critical thinking"

        actual_response_2 = self.client.get(
            "/users/verified?skills=Critical thinking",
            headers=auth_header,
            content_type="application/json",
        )

        for data in json.loads(actual_response_2.data):
            self.assertEqual(expected_response_2, data["skills"])


if __name__ == "__main__":
    unittest.main()
