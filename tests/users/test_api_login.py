import unittest

from flask import json

from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel

# Testing User API resources
#
# TODO tests:
#     - lack of auth token
#     - invalid token
#     - expired token
from tests.test_data import user1, user2


class TestUserLoginApi(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 does not have email verified
    # User 2 has email verified
    def setUp(self):
        super(TestUserLoginApi, self).setUp()

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.second_user = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )
        self.second_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.commit()

    def test_user_login_non_verified_user(self):
        with self.client:
            response = self.client.post('/login', data=json.dumps(dict(
                username=user1['username'],
                password=user1['password']
            )), follow_redirects=True, content_type='application/json')

            self.assertIsNone(response.json.get('access_token'))
            self.assertIsNone(response.json.get('expiry'))
            self.assertEqual(1, len(response.json))
            self.assertEqual('Please verify your email before login.', response.json.get('message', None))
            self.assertEqual(403, response.status_code)

    def test_user_login_verified_user(self):
        with self.client:
            response = self.client.post('/login', data=json.dumps(dict(
                username=user2['username'],
                password=user2['password']
            )), follow_redirects=True, content_type='application/json')
            self.assertIsNotNone(response.json.get('access_token'))
            self.assertIsNotNone(response.json.get('expiry'))
            self.assertEqual(2, len(response.json))
            self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
