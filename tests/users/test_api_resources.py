import unittest
from unittest.mock import patch

from flask import json

from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel


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
                    "POST /register failed to register Testing User! with error code = %d"
                    % response.status_code
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


if __name__ == "__main__":
    unittest.main()
