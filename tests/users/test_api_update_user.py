import unittest
from random import SystemRandom
from string import ascii_lowercase

from flask import json

from app.api.validations.user import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import DB
from app.utils.validation_utils import get_length_validation_error_message
from tests.base_test_case import BaseTestCase
from tests.test_data import USER1
from tests.test_utils import get_test_request_header


class TestUpdateUserApi(BaseTestCase):
    def test_update_user_api_resource_non_auth(self):
        expected_response = {"message": "The authorization token is missing!"}
        actual_response = self.client.put("/user", follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_update_username_already_taken(self):
        # pylint: disable=attribute-defined-outside-init
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

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = {
            "message": "That username is already taken by another user."
        }
        actual_response = self.client.put(
            "/user",
            follow_redirects=True,
            headers=auth_header,
            data=json.dumps(dict(username=self.admin_user.username)),
            content_type="application/json",
        )

        self.assertEqual(400, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_update_username_not_taken(self):

        # pylint: disable=attribute-defined-outside-init
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

        user1_new_username = "new_username"
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = {"message": "User was updated successfully"}
        actual_response = self.client.put(
            "/user",
            follow_redirects=True,
            headers=auth_header,
            data=json.dumps(dict(username=user1_new_username)),
            content_type="application/json",
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))
        self.assertEqual(user1_new_username, self.first_user.username)

    def test_update_username_invalid_length(self):

        # pylint: disable=attribute-defined-outside-init
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

        field_name = "username"
        secure_random = SystemRandom()
        random_generated_username = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(USERNAME_MAX_LENGTH + 1)
        )

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = {
            "message": get_length_validation_error_message(
                field_name, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH
            )
        }
        actual_response = self.client.put(
            "/user",
            follow_redirects=True,
            headers=auth_header,
            data=json.dumps(dict(username=random_generated_username)),
            content_type="application/json",
        )

        self.assertEqual(400, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))
        self.assertNotEqual(
            random_generated_username, self.first_user.username
        )
        self.assertEqual(USER1["username"], self.first_user.username)

    def test_update_availability_to_mentor_more_than_once(self):

        # pylint: disable=attribute-defined-outside-init
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

        expected_response = {"message": "User was updated successfully"}
        test_mentor_availability = True
        auth_header = get_test_request_header(self.first_user.id)

        self.assertEqual(False, self.first_user.available_to_mentor)

        actual_response = self.client.put(
            "/user",
            follow_redirects=True,
            headers=auth_header,
            data=json.dumps(
                dict(available_to_mentor=test_mentor_availability)
            ),
            content_type="application/json",
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

        self.assertEqual(
            test_mentor_availability, self.first_user.available_to_mentor
        )

        actual_response = self.client.put(
            "/user",
            follow_redirects=True,
            headers=auth_header,
            data=json.dumps(
                dict(available_to_mentor=not test_mentor_availability)
            ),
            content_type="application/json",
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

        self.assertEqual(
            not test_mentor_availability, self.first_user.available_to_mentor
        )

    def test_update_availability_to_be_mentee_to_false(self):

        # pylint: disable=attribute-defined-outside-init
        self.first_user = UserModel(
            name=USER1["name"],
            email=USER1["email"],
            username=USER1["username"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        self.first_user.is_email_verified = True
        self.first_user.need_mentoring = True

        DB.session.add(self.first_user)
        DB.session.commit()

        expected_response = {"message": "User was updated successfully"}
        test_need_mentoring = False
        auth_header = get_test_request_header(self.first_user.id)

        self.assertEqual(True, self.first_user.need_mentoring)

        actual_response = self.client.put(
            "/user",
            follow_redirects=True,
            headers=auth_header,
            data=json.dumps(dict(need_mentoring=test_need_mentoring)),
            content_type="application/json",
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))
        self.assertEqual(test_need_mentoring, self.first_user.need_mentoring)


if __name__ == "__main__":
    unittest.main()
