import unittest
from unittest.mock import patch

from flask import json
from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel
from app.messages import (
    USER_WAS_CREATED_SUCCESSFULLY,
    USERNAME_HAS_INVALID_LENGTH,
    PASSWORD_INPUT_BY_USER_HAS_INVALID_LENGTH,
    USER_INPUTS_SPACE_IN_PASSWORD,
    EMAIL_INPUT_BY_USER_IS_INVALID,
    USER_USES_A_USERNAME_THAT_ALREADY_EXISTS,
    USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS,
    TERMS_AND_CONDITIONS_ARE_NOT_CHECKED,
)

# Testing User API resources
#
# TODO tests:
#     - authenticate when User table does not exist
#     - Users GET/POST/PUT/DELETE
#     - Check admin and non admin actions
from tests.test_data import user1


class TestUserRegistrationApi(BaseTestCase):
    def mail_send_mocked(self):
        return self

    # mocking mail.send function which connects with smtp server
    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_without_optional_fields(self, send_email_function):
        # Ensure user registration behaves correctly

        with self.client:
            response = self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password=user1["password"],
                        email=user1["email"],
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )

            user = UserModel.query.filter_by(email=user1["email"]).first()
            if user is None:
                self.fail(
                    f"POST /register failed to register Testing User! with error code = {response.status_code}"
                )
            else:
                self.assertEqual(user1["name"], user.name)
                self.assertEqual(user1["username"], user.username)
                self.assertEqual(user1["email"], user.email)
                self.assertEqual(
                    user1["terms_and_conditions_checked"],
                    user.terms_and_conditions_checked,
                )
                self.assertFalse(user.is_admin)
                self.assertFalse(user.is_email_verified)
                self.assertFalse(user.need_mentoring)
                self.assertFalse(user.available_to_mentor)

    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_with_both_optional_fields(self, send_email_function):
        with self.client:
            self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password=user1["password"],
                        email=user1["email"],
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                        available_to_mentor=user1["available_to_mentor"],
                        need_mentoring=user1["need_mentoring"],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )

            user = UserModel.query.filter_by(email=user1["email"]).first()
            self.assertTrue(user.need_mentoring)
            self.assertTrue(user.available_to_mentor)

    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_mentor(self, send_email_function):
        with self.client:
            self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password=user1["password"],
                        email=user1["email"],
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                        available_to_mentor=user1["available_to_mentor"],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )

            user = UserModel.query.filter_by(email=user1["email"]).first()
            self.assertFalse(user.need_mentoring)
            self.assertTrue(user.available_to_mentor)

    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_mentee(self, send_email_function):
        with self.client:
            self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password=user1["password"],
                        email=user1["email"],
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                        need_mentoring=user1["need_mentoring"],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )

            user = UserModel.query.filter_by(email=user1["email"]).first()
            self.assertTrue(user.need_mentoring)
            self.assertFalse(user.available_to_mentor)

    # new tests to verify response status codes
    # BAD_REQUEST status
    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_with_invalid_length_username(self, send_email_function):
        with self.client:
            # invalid username and password length
            response = self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username="test",
                        password=user1["email"],
                        email=user1["email"],
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )

            user = UserModel.query.filter_by(username="test").first()
            message = json.loads(response.get_data(as_text=True)).get("message")
            self.assertIsNone(user)
            self.assertEqual(message, USERNAME_HAS_INVALID_LENGTH.get("message"))
            self.assertEqual(response.status_code, 400)

    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_with_invalid_length_password(self, send_email_function):
        with self.client:
            # invalid username and password length
            response = self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password="test",
                        email=user1["email"],
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )

            user = UserModel.query.filter_by(username=user1["username"]).first()
            message = json.loads(response.get_data(as_text=True)).get("message")
            self.assertIsNone(user)
            self.assertEqual(
                message, PASSWORD_INPUT_BY_USER_HAS_INVALID_LENGTH.get("message")
            )
            self.assertEqual(response.status_code, 400)

    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_with_space_in_password(self, send_email_function):
        with self.client:
            # invalid username and password length
            response = self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password="test password",
                        email=user1["email"],
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )

            user = UserModel.query.filter_by(username=user1["username"]).first()
            message = json.loads(response.get_data(as_text=True)).get("message")
            self.assertIsNone(user)
            self.assertEqual(message, USER_INPUTS_SPACE_IN_PASSWORD.get("message"))
            self.assertEqual(response.status_code, 400)

    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_with_invalid_email(self, send_email_function):
        with self.client:
            # invalid username and password length
            response = self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password=user1["password"],
                        email="testemail",
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )
            message = json.loads(response.get_data(as_text=True)).get("message")
            user = UserModel.query.filter_by(email="testemail").first()
            self.assertIsNone(user)
            self.assertEqual(message, EMAIL_INPUT_BY_USER_IS_INVALID.get("message"))
            self.assertEqual(response.status_code, 400)

    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_with_unckecked_terms_and_conditions(
        self, send_email_function
    ):
        with self.client:
            # invalid username and password length
            response = self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password=user1["password"],
                        email="testemail",
                        terms_and_conditions_checked=False,
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )
            message = json.loads(response.get_data(as_text=True)).get("message")
            user = UserModel.query.filter_by(username=user1["username"]).first()
            self.assertIsNone(user)
            self.assertEqual(
                message, TERMS_AND_CONDITIONS_ARE_NOT_CHECKED.get("message")
            )
            self.assertEqual(response.status_code, 400)

    # CONFLICT status code
    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_with_taken_username(self, send_email_function):
        user = UserModel.query.first()
        username = user.username
        with self.client:
            response = self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=username,
                        password=user1["password"],
                        email=user1["email"],
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )
            message = json.loads(response.get_data(as_text=True)).get("message")
            users_count = UserModel.query.filter_by(username=username).count()
            self.assertEqual(users_count, 1)
            self.assertEqual(
                message, USER_USES_A_USERNAME_THAT_ALREADY_EXISTS.get("message")
            )
            self.assertEqual(response.status_code, 409)

    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_user_registration_with_taken_email(self, send_email_function):
        user = UserModel.query.first()
        email = user.email
        with self.client:
            response = self.client.post(
                "/register",
                data=json.dumps(
                    dict(
                        name=user1["name"],
                        username=user1["username"],
                        password=user1["password"],
                        email=email,
                        terms_and_conditions_checked=user1[
                            "terms_and_conditions_checked"
                        ],
                    )
                ),
                follow_redirects=True,
                content_type="application/json",
            )
            message = json.loads(response.get_data(as_text=True)).get("message")
            users_count = UserModel.query.filter_by(email=email).count()
            self.assertEqual(users_count, 1)
            self.assertEqual(
                message, USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS.get("message")
            )
            self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
