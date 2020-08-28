import unittest

from flask import json
from http import HTTPStatus
from app import messages
from app.database.sqlalchemy_extension import db
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2, test_admin_user


class TestResendEmail(BaseTestCase):

    def setUp(self):
        super(TestResendEmail, self).setUp()
        self.resend_url = '/user/resend_email'
        self.first_user = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        db.session.add(self.first_user)
        db.session.commit()

    def test_confirm_email(self):
        """
        calling resend_email for a new user and validate the responses
        """
        resp = self.client.post(self.resend_url, data=json.dumps({'email': user1['email']}),
                                content_type='application/json')
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(messages.EMAIL_VERIFICATION_MESSAGE, json.loads(resp.data))
        user = UserModel.find_by_email(user1['email'])
        self.assertEqual(False, user.is_email_verified)

    def test_confirmed_user_send_email(self):
        """
        calling resend_email for a user whose email is validated
        """
        resp = self.client.post(self.resend_url, data=json.dumps({'email': test_admin_user['email']}),
                                content_type='application/json')
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)
        self.assertEqual(messages.USER_ALREADY_CONFIRMED_ACCOUNT, json.loads(resp.data))

    def test_wrong_user(self):
        """
        calling resend_email for an unknown email
        """
        resp = self.client.post(self.resend_url, data=json.dumps({'email': user2['email']}),
                                content_type='application/json')
        self.assertEqual(HTTPStatus.NOT_FOUND, resp.status_code)
        self.assertEqual(messages.USER_DOES_NOT_EXIST, json.loads(resp.data))

    def test_invalid_email(self):
        """
        calling resend_email with an invalid email id
        """
        resp = self.client.post(self.resend_url, data=json.dumps({'email': 'invalid_email'}),
                                content_type='application/json')
        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status_code)
        self.assertEqual(messages.EMAIL_INPUT_BY_USER_IS_INVALID, json.loads(resp.data))


if __name__ == '__main__':
    unittest.main()
